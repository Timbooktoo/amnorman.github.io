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
def list_recordings_by_date(from_date: str, to_date: str) -> list[dict]:
    """
    Geef opnames binnen een datumbereik.

    Args:
        from_date: Startdatum in ISO-formaat, bijv. "2024-01-01" of "2024-01-01T00:00:00".
        to_date:   Einddatum in ISO-formaat, bijv. "2024-01-31" of "2024-01-31T23:59:59".

    Returns:
        Lijst van opnames (zelfde velden als list_recordings) die binnen het bereik vallen.
    """
    return client.list_recordings_by_date(from_date, to_date)


@mcp.tool()
def search_recordings(query: str) -> list[dict]:
    """
    Zoek opnames op titel of keyword.

    Args:
        query: Zoekterm (hoofdletterongevoelig).

    Returns:
        Lijst van overeenkomende opnames.
    """
    return client.search_recordings(query)


@mcp.tool()
def get_summary(recording_id: str) -> dict:
    """
    Haal de AI-samenvatting op van een opname.

    Args:
        recording_id: Het id van de opname (verkregen via list_recordings).

    Returns:
        Dict met id, title, duration_seconds, recorded_at en summary.
    """
    return client.get_summary(recording_id)


@mcp.tool()
def get_transcript(recording_id: str) -> dict:
    """
    Haal de volledige transcriptie op van een opname.

    Args:
        recording_id: Het id van de opname (verkregen via list_recordings).

    Returns:
        Dict met id, title, duration_seconds, recorded_at en transcript.
    """
    return client.get_transcript(recording_id)


@mcp.tool()
def get_audio_url(recording_id: str) -> dict:
    """
    Geef een tijdelijke MP3-downloadlink voor een opname.

    Args:
        recording_id: Het id van de opname (verkregen via list_recordings).

    Returns:
        Dict met recording_id en url (tijdelijke download-URL).
    """
    return client.get_audio_url(recording_id)


@mcp.tool()
def get_user_info() -> dict:
    """
    Geef accountinformatie van de ingelogde Plaud-gebruiker.

    Returns:
        Dict met id, name, email, country en membership.
    """
    return client.get_user_info()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
