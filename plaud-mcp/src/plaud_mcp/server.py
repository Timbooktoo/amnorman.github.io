from mcp.server.fastmcp import FastMCP

from . import client

mcp = FastMCP("Plaud Note")


@mcp.tool()
def list_recordings(limit: int = 50) -> list[dict]:
    """
    Geef een overzicht van Plaud Note opnames.

    Args:
        limit: Maximum aantal opnames om op te halen (standaard 50).

    Returns:
        Lijst van opnames met id, title, duration_seconds, recorded_at,
        has_summary en keywords.
    """
    return client.list_recordings(limit=limit)


@mcp.tool()
def get_summary(recording_id: str) -> dict:
    """
    Haal de samenvatting (en transcriptie) op van een specifieke opname.

    Args:
        recording_id: Het id van de opname (verkregen via list_recordings).

    Returns:
        Dict met id, title, duration_seconds, recorded_at, summary en transcript.
    """
    return client.get_detail(recording_id)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
