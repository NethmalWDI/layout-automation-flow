#!/usr/bin/env node
// docker-eda: a deliberately narrow MCP server for the layout-automation-s0-s3 project.
//
// It lets Claude manage and run commands inside TWO named containers only:
//   layout-s0s3   (hpretl/iic-osic-tools:2026.10)  repo mounted at /foss/designs
//   magical-s0s3  (jayl940712/magical:latest)      repo mounted at /work
//
// Safety properties (enforced in code, not by convention):
//   * docker is spawned directly with an argument array: no host shell, so no
//     host-side command injection. Nothing ever runs on Windows except `docker`.
//   * Only the container names above are accepted; any other container (e.g. your
//     existing iic-osic-tools_xserver) cannot be started, stopped, exec'd or removed.
//   * Images and bind mounts are fixed below; only this repository folder is mounted.
//   * No published ports, no --privileged, no host network, no docker.sock mount.
//   * There is no generic `docker` passthrough and no image/volume/system prune.
//   * Removal is limited to containers carrying this server's label.

import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const HERE = path.dirname(fileURLToPath(import.meta.url));
// tools/mcp-docker-eda/server.mjs -> repository root is two levels up
const REPO_HOST = process.env.DOCKER_EDA_REPO || path.resolve(HERE, "..", "..");
const LABEL = "created-by=mcp-docker-eda";

const CONTAINERS = {
  "layout-s0s3": { image: "hpretl/iic-osic-tools:2026.10", mount: "/foss/designs" },
  "magical-s0s3": { image: "jayl940712/magical:latest", mount: "/work" },
};
const NAMES = Object.keys(CONTAINERS);
const MAX_OUT = 60000;

function runDocker(args, timeoutMs = 120000) {
  return new Promise((resolve) => {
    const p = spawn("docker", args, { shell: false, windowsHide: true });
    let out = "", err = "", killed = false;
    const t = setTimeout(() => { killed = true; p.kill(); }, timeoutMs);
    p.stdout.on("data", (d) => { out += d; if (out.length > 4 * MAX_OUT) out = out.slice(-2 * MAX_OUT); });
    p.stderr.on("data", (d) => { err += d; if (err.length > 4 * MAX_OUT) err = err.slice(-2 * MAX_OUT); });
    p.on("error", (e) => { clearTimeout(t); resolve({ code: -1, out, err: String(e), killed }); });
    p.on("close", (code) => { clearTimeout(t); resolve({ code, out, err, killed }); });
  });
}

function fmt(r, label = "") {
  const tail = (s) => (s.length > MAX_OUT ? "...[truncated]...\n" + s.slice(-MAX_OUT) : s);
  return {
    content: [{
      type: "text",
      text: `${label}exit_code: ${r.code}${r.killed ? " (killed: timeout)" : ""}\n--- stdout ---\n${tail(r.out)}\n--- stderr ---\n${tail(r.err)}`,
    }],
  };
}

const nameSchema = z.enum(NAMES).describe("One of the allow-listed container names");

const server = new McpServer({ name: "docker-eda", version: "0.1.0" });

server.registerTool("docker_status", {
  description: "Docker version, the allow-listed containers' state, and whether their images are present locally.",
  inputSchema: {},
}, async () => {
  const v = await runDocker(["version", "--format", "client {{.Client.Version}} / server {{.Server.Version}}"]);
  const lines = [`repo_host: ${REPO_HOST}`, `docker: ${v.out.trim() || v.err.trim()}`];
  for (const n of NAMES) {
    const ps = await runDocker(["ps", "-a", "--filter", `name=^${n}$`, "--format", "{{.Names}}  {{.Image}}  {{.Status}}"]);
    lines.push(`container ${n}: ${ps.out.trim() || "(not created)"}`);
    const im = await runDocker(["image", "ls", CONTAINERS[n].image, "--format", "{{.Repository}}:{{.Tag}}  {{.ID}}  {{.Size}}"]);
    lines.push(`  image ${CONTAINERS[n].image}: ${im.out.trim() || "(not pulled)"}`);
  }
  return { content: [{ type: "text", text: lines.join("\n") }] };
});

server.registerTool("container_create", {
  description: "Create and start an allow-listed container from its fixed image (pulls it if needed), mounting only this repository at the fixed path. Keeps running with `sleep infinity`; no ports are published.",
  inputSchema: { name: nameSchema },
}, async ({ name }) => {
  const c = CONTAINERS[name];
  const exists = await runDocker(["ps", "-a", "-q", "--filter", `name=^${name}$`]);
  if (exists.out.trim()) return { content: [{ type: "text", text: `${name} already exists; use container_start.` }] };
  const args = ["run", "-d", "--name", name, "--label", LABEL,
    "-v", `${REPO_HOST}:${c.mount}:rw`, "-w", c.mount,
    "--entrypoint", "sleep", c.image, "infinity"];
  return fmt(await runDocker(args, 3600000), `docker ${args.join(" ")}\n`);
});

server.registerTool("container_start", {
  description: "Start an allow-listed container.",
  inputSchema: { name: nameSchema },
}, async ({ name }) => fmt(await runDocker(["start", name])));

server.registerTool("container_stop", {
  description: "Stop an allow-listed container.",
  inputSchema: { name: nameSchema },
}, async ({ name }) => fmt(await runDocker(["stop", name])));

server.registerTool("container_exec", {
  description: "Run a bash command inside an allow-listed container and wait for it (max 15 min). For longer jobs use container_exec_background and read the log from the repo folder.",
  inputSchema: {
    name: nameSchema,
    command: z.string().min(1).describe("Passed to `bash -c` inside the container"),
    as_root: z.boolean().default(false).describe("Run as root inside the container (e.g. apt install there)"),
    workdir: z.string().optional().describe("Working directory inside the container"),
    timeout_s: z.number().int().min(5).max(900).default(300),
  },
}, async ({ name, command, as_root, workdir, timeout_s }) => {
  const args = ["exec"];
  if (as_root) args.push("-u", "0");
  if (workdir) args.push("-w", workdir);
  args.push(name, "bash", "-c", command);
  return fmt(await runDocker(args, timeout_s * 1000));
});

server.registerTool("container_exec_background", {
  description: "Start a long bash command detached inside an allow-listed container. stdout+stderr go to log_path (relative to the repo mount) and the exit code to log_path + '.exit' when it finishes.",
  inputSchema: {
    name: nameSchema,
    command: z.string().min(1),
    log_path: z.string().regex(/^[A-Za-z0-9_.\/-]+$/).describe("Relative path inside the repo, e.g. runs/logs/align_install.log"),
    as_root: z.boolean().default(false),
  },
}, async ({ name, command, log_path, as_root }) => {
  if (log_path.includes("..") || log_path.startsWith("/")) {
    return { content: [{ type: "text", text: "log_path must be relative to the repo and must not contain '..'" }] };
  }
  const mount = CONTAINERS[name].mount;
  const log = `${mount}/${log_path}`;
  const wrapped = `mkdir -p "$(dirname '${log}')"; rm -f '${log}.exit'; ( ${command} ) > '${log}' 2>&1; echo $? > '${log}.exit'`;
  const args = ["exec", "-d"];
  if (as_root) args.push("-u", "0");
  args.push(name, "bash", "-c", wrapped);
  return fmt(await runDocker(args), `started; log: ${log_path}\n`);
});

server.registerTool("container_remove", {
  description: "Remove an allow-listed container, only if it was created by this server (label check). The image and the repository files are not touched.",
  inputSchema: { name: nameSchema, confirm: z.literal(true) },
}, async ({ name }) => {
  const lab = await runDocker(["inspect", "--format", "{{index .Config.Labels \"created-by\"}}", name]);
  if (lab.out.trim() !== "mcp-docker-eda") {
    return { content: [{ type: "text", text: `${name} was not created by this server; refusing to remove.` }] };
  }
  return fmt(await runDocker(["rm", "-f", name]));
});

await server.connect(new StdioServerTransport());
