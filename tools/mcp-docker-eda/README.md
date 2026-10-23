# docker-eda: Claude's narrow MCP server for Docker

This server lets Claude (through Claude Desktop) create and run commands in **two named containers and nothing else**:

| Container | Image | Repo mounted at |
|---|---|---|
| `layout-s0s3` | `hpretl/iic-osic-tools:2026.10` | `/foss/designs` |
| `magical-s0s3` | `jayl940712/magical:latest` | `/work` |

## What it cannot do

These limits are enforced in `server.mjs`:

- Touch any other container. Your existing `iic-osic-tools_xserver` is rejected by name validation.
- Run anything on Windows except the `docker` executable. There is no shell, and arguments are passed as an array.
- Publish ports, use `--privileged`, mount anything except this repository, prune images or volumes, or remove containers it did not create.

## One-time setup on Windows

1. **Install dependencies.** Open PowerShell and run:

   ```powershell
   cd C:\Users\suind\Documents\GitHub\layout-automation-s0-s3\tools\mcp-docker-eda
   npm install
   ```

   This installs two pinned packages (`@modelcontextprotocol/sdk` 1.32.1 and `zod` 3.25.76) into `node_modules` here.

2. **Open the Claude Desktop config.** In Claude Desktop, go to **Settings → Developer → Edit Config**. This opens `claude_desktop_config.json`.

3. **Add the server entry.** Add the block below. If the file already has a `"mcpServers"` section, add only the `"docker-eda"` entry inside it.

   ```json
   {
     "mcpServers": {
       "docker-eda": {
         "command": "node",
         "args": ["C:\\Users\\suind\\Documents\\GitHub\\layout-automation-s0-s3\\tools\\mcp-docker-eda\\server.mjs"]
       }
     }
   }
   ```

4. **Restart Claude Desktop.** First make sure **Docker Desktop is running**. Then fully quit Claude Desktop and reopen it. Closing the window with **X** is not enough: Claude keeps running in the background, so it never re-reads the config. To quit fully, use one of these:
   - **Tray icon:** click the **^** arrow at the bottom-right of the taskbar (next to the clock), right-click the **Claude** icon, and choose **Quit**.
   - **App menu:** in the Claude window, click the **☰** menu (top-left), then **File → Exit**.
   - **Task Manager:** press **Ctrl+Shift+Esc**, select every **Claude** process, and click **End task**.

   After that, start Claude Desktop again from the Start menu.

5. **Check the server is running.** Under **Settings → Developer**, `docker-eda` should show as running.

6. **Tell Claude it's ready.** The tools appear to Claude as `docker_status`, `container_create`, `container_start`, `container_stop`, `container_exec`, `container_exec_background` and `container_remove`.

## How to undo it

1. Delete the `"docker-eda"` entry from the config and restart Claude Desktop.
2. To remove the containers:

   ```powershell
   docker rm -f layout-s0s3 magical-s0s3
   ```

3. To remove the MAGICAL image:

   ```powershell
   docker image rm jayl940712/magical:latest
   ```

   Do **not** remove `hpretl/iic-osic-tools:2026.10`. Your other container uses it.
