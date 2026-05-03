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
      "args": ["plaud-mcp"],
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
