from datetime import datetime, timezone

import httpx

from .auth import BASE_URL, auth_headers


def _get(path: str, params: dict | None = None) -> dict:
    response = httpx.get(
        f"{BASE_URL}{path}",
        params=params,
        headers=auth_headers(),
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()
    if body.get("status", -1) != 0:
        raise RuntimeError(f"API fout op {path}: {body}")
    return body


def _ms_to_iso(ms: int | None) -> str | None:
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()


def list_recordings(limit: int = 50) -> list[dict]:
    body = _get(
        "/file/simple/web",
        params={
            "skip": 0,
            "limit": limit,
            "is_trash": 0,
            "sort_by": "edit_time",
            "is_desc": "true",
        },
    )
    recordings = []
    for item in body.get("list", []):
        recordings.append(
            {
                "id": item.get("id"),
                "title": item.get("filename"),
                "duration_seconds": item.get("duration"),
                "recorded_at": _ms_to_iso(item.get("start_time")),
                "has_summary": item.get("is_summary", False),
                "keywords": item.get("keywords", []),
            }
        )
    return recordings


def get_detail(recording_id: str) -> dict:
    body = _get(f"/file/detail/{recording_id}")
    return {
        "id": body.get("id"),
        "title": body.get("filename"),
        "duration_seconds": body.get("duration"),
        "recorded_at": _ms_to_iso(body.get("start_time")),
        "summary": body.get("summary"),
        "transcript": body.get("transcript"),
    }
