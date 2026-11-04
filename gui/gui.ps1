<#
  The flow's local GUI (Imasha, 2026-11-04). Windows PowerShell 5.1 or later; nothing to install.

    .\gui\gui.ps1                 then open http://localhost:8765/ in a browser
    .\gui\gui.ps1 -Port 8800      another port

  It serves gui/index.html on this PC only (localhost) and runs everything inside the flow's Docker container
  through `docker exec`, as flow.ps1 does: scripts/gui_backend.py (list, load and save designs),
  `python3 -m src.flow run` and scripts/make_design_report.py. No LLM is called. Stop it with Ctrl+C.

  Safety:
    * an edit is saved as a NEW design copy; the original's files and results are never changed; a brand-new
      design can be made from uploaded files (netlist, specs, optional benches, hierarchy, layout instructions,
      any other files, kept in circuits/<design>/extra/);
    * the flow runs only on designs made with this GUI (their package.yaml says so), so the committed results of
      ttsky25a_fd, the 5T, LOADBench and the others cannot be overwritten from here; reports only read outputs;
    * files are served only from docs/ and outputs/report/.
#>
param([int]$Port = 8765, [string]$Container = $(if ($env:FLOW_CONTAINER) { $env:FLOW_CONTAINER } else { "layout-s0s3" }))

$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $PSScriptRoot
$Utf8 = New-Object System.Text.UTF8Encoding $false
$NameRx = '^[a-z][a-z0-9_]{1,40}$'

function Invoke-Backend([string]$ArgLine) {
    $cmd = "cd /foss/designs && source scripts/env.sh >/dev/null 2>&1 && python3 scripts/gui_backend.py $ArgLine"
    $lines = & docker exec -e IIC_OSIC_TOOLS_QUIET=1 $Container bash -lc $cmd 2>$null
    $json = @($lines) | Where-Object { $_ -like '{*' } | Select-Object -Last 1
    if (-not $json) { return '{"ok": false, "errors": ["the container did not answer: is layout-s0s3 running?"]}' }
    return $json
}

function Start-Detached([string]$Shell) {
    & docker exec -d -e IIC_OSIC_TOOLS_QUIET=1 $Container bash -lc "cd /foss/designs && source scripts/env.sh && $Shell" | Out-Null
}

function Test-GuiDesign([string]$Design) {
    $pkg = Join-Path $Repo "inputs\$Design\package.yaml"
    if (-not (Test-Path $pkg)) { return $false }
    $first = Get-Content $pkg -TotalCount 1
    return ($first -like '*made with the local GUI*')   # a copy or a new design made here
}

function Send-Response($Ctx, [int]$Code, [string]$Type, [byte[]]$Bytes) {
    $r = $Ctx.Response
    $r.StatusCode = $Code
    $r.ContentType = $Type
    $r.Headers.Add("Cache-Control", "no-store")
    $r.ContentLength64 = $Bytes.Length
    $r.OutputStream.Write($Bytes, 0, $Bytes.Length)
    $r.OutputStream.Close()
}

function Send-Json($Ctx, [string]$Json, [int]$Code = 200) {
    Send-Response $Ctx $Code "application/json; charset=utf-8" ($Utf8.GetBytes($Json))
}

function Read-Body($Ctx) {
    $sr = New-Object System.IO.StreamReader($Ctx.Request.InputStream, $Utf8)
    $t = $sr.ReadToEnd()
    $sr.Close()
    return $t
}

$types = @{ ".html" = "text/html; charset=utf-8"; ".png" = "image/png"; ".svg" = "image/svg+xml";
            ".css" = "text/css"; ".js" = "text/javascript"; ".json" = "application/json"; ".md" = "text/plain; charset=utf-8" }

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()
Write-Host "Layout flow GUI: http://localhost:$Port/   (container $Container; Ctrl+C to stop)"

try {
    while ($listener.IsListening) {
        $ctx = $listener.GetContext()
        $path = $ctx.Request.Url.AbsolutePath
        $method = $ctx.Request.HttpMethod
        try {
            if ($path -eq "/" -or $path -eq "/index.html") {
                Send-Response $ctx 200 "text/html; charset=utf-8" ([IO.File]::ReadAllBytes((Join-Path $PSScriptRoot "index.html")))
            }
            elseif ($path -eq "/api/designs") {
                Send-Json $ctx (Invoke-Backend "list")
            }
            elseif ($path -eq "/api/design" -or $path -eq "/api/status") {
                $d = $ctx.Request.QueryString["name"]
                if ($d -notmatch $NameRx) { Send-Json $ctx '{"ok": false, "errors": ["bad design name"]}' 400; continue }
                $j = Invoke-Backend ("{0} {1}" -f ($(if ($path -eq "/api/design") { "get" } else { "status" })), $d)
                if ($path -eq "/api/status") {
                    $g = if (Test-GuiDesign $d) { "true" } else { "false" }
                    $j = $j.TrimEnd().TrimEnd('}') + ", `"gui_design`": $g}"
                }
                Send-Json $ctx $j
            }
            elseif (($path -eq "/api/save" -or $path -eq "/api/new" -or $path -eq "/api/template") -and $method -eq "POST") {
                $dir = Join-Path $Repo "runs\tmp\gui"
                New-Item -ItemType Directory -Force $dir | Out-Null
                $name = "req_{0}.json" -f [DateTime]::Now.Ticks
                [IO.File]::WriteAllText((Join-Path $dir $name), (Read-Body $ctx), $Utf8)
                Send-Json $ctx (Invoke-Backend ("{0} runs/tmp/gui/{1}" -f $path.Substring(5), $name))
            }
            elseif (($path -eq "/api/run" -or $path -eq "/api/report") -and $method -eq "POST") {
                $req = (Read-Body $ctx) | ConvertFrom-Json
                $d = [string]$req.design
                if ($d -notmatch $NameRx) { Send-Json $ctx '{"ok": false, "errors": ["bad design name"]}' 400; continue }
                $rep = "rm -f runs/logs/gui_${d}_report.log.exit; python3 scripts/make_design_report.py $d > runs/logs/gui_${d}_report.log 2>&1; echo `$? > runs/logs/gui_${d}_report.log.exit"
                if ($path -eq "/api/report") {
                    Start-Detached $rep
                    Send-Json $ctx '{"ok": true}'
                    continue
                }
                if (-not (Test-GuiDesign $d)) {
                    Send-Json $ctx '{"ok": false, "errors": ["the GUI runs the flow only on designs it made (save an edit as a new design first); the committed designs run with flow.ps1"]}'
                    continue
                }
                $from = [string]$req.from
                if ($from -notmatch '^S[0-7]$') { $from = "S0" }
                $st = Invoke-Backend "status $d" | ConvertFrom-Json
                if ($st.running) { Send-Json $ctx '{"ok": false, "errors": ["a run of this design is still going"]}'; continue }
                Start-Detached ("rm -f runs/logs/gui_$d.log.exit runs/logs/gui_${d}_report.log.exit runs/logs/gui_${d}_report.log; " +
                                "python3 -m src.flow run $d --from $from > runs/logs/gui_$d.log 2>&1; " +
                                "echo `$? > runs/logs/gui_$d.log.exit; $rep")
                Send-Json $ctx '{"ok": true}'
            }
            elseif ($path.StartsWith("/files/")) {
                $rel = [Uri]::UnescapeDataString($path.Substring(7)).Replace("/", "\")
                $full = [IO.Path]::GetFullPath((Join-Path $Repo $rel))
                $okRoots = @((Join-Path $Repo "docs\"), (Join-Path $Repo "outputs\report\"), (Join-Path $Repo "outputs\S"))
                $allowed = $false
                foreach ($root in $okRoots) { if ($full.StartsWith($root, [StringComparison]::OrdinalIgnoreCase)) { $allowed = $true } }
                if (-not $allowed -or -not (Test-Path $full -PathType Leaf)) { Send-Response $ctx 404 "text/plain" ($Utf8.GetBytes("not found")); continue }
                $ext = [IO.Path]::GetExtension($full).ToLower()
                $type = if ($types.ContainsKey($ext)) { $types[$ext] } else { "application/octet-stream" }
                Send-Response $ctx 200 $type ([IO.File]::ReadAllBytes($full))
            }
            else {
                Send-Response $ctx 404 "text/plain" ($Utf8.GetBytes("not found"))
            }
        }
        catch {
            $msg = ($_.Exception.Message -replace '"', "'")
            try { Send-Json $ctx "{`"ok`": false, `"errors`": [`"server error: $msg`"]}" 500 } catch {}
        }
    }
}
finally {
    $listener.Stop()
}
