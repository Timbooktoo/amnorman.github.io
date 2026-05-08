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
        "PLAUD_EMAIL": "your@email.com",
        "PLAUD_PASSWORD": "yourpassword"
      }
    }
  }
}
```

### 2. Restart Claude Desktop

On first use, the server logs in and caches the token at `~/.plaud/config.json`. The token is valid for ~300 days and refreshes automatically.

## Troubleshooting Claude Desktop

If Claude cannot start the server with `uvx`, check that `uvx` is available to Claude:

- macOS / Linux: run `which uvx`
- Windows: run `Get-Command uvx`

If needed, replace `"command": "uvx"` with the full path to `uvx.exe`, for example:

```json
"command": "C:\\Users\\your-user\\.local\\bin\\uvx.exe"
```

If Claude shows `Server disconnected`, make sure the arguments are three separate strings:

```json
"args": [
  "--from",
  "git+https://github.com/Timbooktoo/amnorman.github.io#subdirectory=plaud-mcp",
  "plaud-mcp"
]
```

Do not enter them as one combined string like:

```json
"args": ["--from git+https://github.com/Timbooktoo/amnorman.github.io#subdirectory=plaud-mcp plaud-mcp"]
```

Do not use `uvx plaud-mcp` unless the package has been published to PyPI. This repo currently runs it from GitHub with `--from git+https://github.com/Timbooktoo/amnorman.github.io#subdirectory=plaud-mcp`.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- A Plaud Note account

## Authentication

Credentials are read from environment variables:

| Variable | Description |
|---|---|
| `PLAUD_EMAIL` | Your Plaud account email |
| `PLAUD_PASSWORD` | Your Plaud account password |

> **Note:** This package uses the reverse-engineered Plaud web API. It is not affiliated with Plaud Inc.

## License

MIT
