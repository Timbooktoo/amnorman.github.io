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
        "PLAUD_TOKEN": "your-bearer-token"
      }
    }
  }
}
```

On Windows, `uvx` may not be on Claude Desktop's PATH. Replace `"command": "uvx"` with the full path (run `where.exe uvx` in PowerShell to find it). If `uvx` fails entirely, see [Installing without uvx](#installing-without-uvx).

### 2. Restart Claude Desktop

Fully quit (system tray → Quit) and reopen.

## Authentication

Credentials are read from environment variables. Two options — use whichever suits you:

| Variable | Description |
|---|---|
| `PLAUD_TOKEN` | Your Plaud bearer token (recommended) |
| `PLAUD_EMAIL` + `PLAUD_PASSWORD` | Your Plaud account credentials |

`PLAUD_TOKEN` takes priority if both are set. When using email/password, the server logs in on first use and caches the token at `~/.plaud/config.json` (valid ~300 days, auto-refreshes).

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
