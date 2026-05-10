# plaud-mcp

MCP server for [Plaud Note](https://www.plaud.ai) — gives Claude access to your recordings, summaries, and transcripts.

## Tools

| Tool | Description |
|---|---|
| `list_recordings` | List all recordings with metadata |
| `list_recordings_by_date` | Filter recordings by date range |
| `search_recordings` | Search by title or keyword |
| `get_summary` | Get the AI summary of a recording |
| `get_transcript` | Get the full transcript of a recording |
| `get_audio_url` | Get a temporary MP3 download link |
| `get_user_info` | Get account info |

## Setup

### 1. Add to Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "plaud": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Timbooktoo/amnorman.github.io#subdirectory=plaud-mcp",
        "plaud-mcp"
      ],
      "env": {
        "PLAUD_TOKEN": "your-bearer-token",
        "PLAUD_USER_ID": "your-x-pld-user-value"
      }
    }
  }
}
```

On Windows, `uvx` may not be on Claude Desktop's PATH. Replace `"command": "uvx"` with the full path (run `where.exe uvx` in PowerShell to find it). If `uvx` fails entirely, see [Installing without uvx](#installing-without-uvx).

### 2. Restart Claude Desktop

Fully quit (system tray → Quit) and reopen.

## Authentication

Plaud's API rejects requests that lack the right combination of bearer token and custom headers. Both `PLAUD_TOKEN` and `PLAUD_USER_ID` are required — the rest have sensible defaults.

| Variable | Required | Description |
|---|---|---|
| `PLAUD_TOKEN` | yes | Bearer JWT (without the `Bearer ` prefix) |
| `PLAUD_USER_ID` | yes | The 64-char hex value Plaud sends as `x-pld-user` header |
| `PLAUD_DEVICE_ID` | no | Defaults to literal `[object Object]` (a quirk in Plaud's frontend that the backend requires) |
| `PLAUD_TIMEZONE` | no | Defaults to `Europe/Brussels` |
| `PLAUD_EMAIL` + `PLAUD_PASSWORD` | no | Enables automatic token refresh via the `/auth/access-token` endpoint when the bearer token expires or is revoked |

### Where to find PLAUD_TOKEN and PLAUD_USER_ID

1. Open <https://web.plaud.ai> and log in
2. Open browser DevTools (F12) → **Network** tab → enable **Preserve log**
3. Click around in the UI to trigger an API call (e.g. open *My Files*)
4. Click any successful request to `api.plaud.ai/...` (HTTP 200)
5. Under **Request Headers**, copy:
   - `authorization: Bearer eyJ...` → take the part after `Bearer ` → this is your `PLAUD_TOKEN`
   - `x-pld-user: <hex>` → this is your `PLAUD_USER_ID`

The token's lifetime varies — current tokens issued via web login are valid roughly 300 days, but Plaud may revoke them server-side after logout or password change. If you set `PLAUD_EMAIL` + `PLAUD_PASSWORD`, the server re-logs in automatically when the API rejects the cached token; otherwise you'll need to refresh `PLAUD_TOKEN` manually from DevTools.

## Installing without uvx

If `uvx` fails (common on Windows due to git resolution issues), install once with pip instead:

```
pip install "git+https://github.com/Timbooktoo/amnorman.github.io#subdirectory=plaud-mcp"
```

Then find the installed script path:
- **Windows:** `where.exe plaud-mcp`
- **macOS/Linux:** `which plaud-mcp`

Use that full path as `"command"` in your config with `"args": []`.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A Plaud Note account

## License

MIT
