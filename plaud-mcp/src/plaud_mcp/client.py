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


def _format_recording(item: dict) -> dict:
    return {
        "id": item.get("id"),
        "title": item.get("filename"),
        "duration_seconds": item.get("duration"),
        "recorded_at": _ms_to_iso(item.get("start_time")),
        "has_summary": item.get("is_summary", False),
        "keywords": item.get("keywords", []),
    }


def _fetch_all_recordings(limit: int = 9999) -> list[dict]:
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
    return body.get("list", [])


def list_recordings(limit: int = 50) -> list[dict]:
    return [_format_recording(item) for item in _fetch_all_recordings(limit)]


def list_recordings_by_date(from_date: str, to_date: str) -> list[dict]:
    from_dt = datetime.fromisoformat(from_date).replace(tzinfo=timezone.utc)
    to_dt = datetime.fromisoformat(to_date).replace(tzinfo=timezone.utc)
    from_ms = int(from_dt.timestamp() * 1000)
    to_ms = int(to_dt.timestamp() * 1000)

    items = _fetch_all_recordings()
    results = []
    for item in items:
        start = item.get("start_time", 0)
        if from_ms <= start <= to_ms:
            results.append(_format_recording(item))
    return results


def search_recordings(query: str) -> list[dict]:
    q = query.lower()
    items = _fetch_all_recordings()
    results = []
    for item in items:
        title = (item.get("filename") or "").lower()
        keywords = [k.lower() for k in item.get("keywords") or []]
        if q in title or any(q in k for k in keywords):
            results.append(_format_recording(item))
    return results


def get_summary(recording_id: str) -> dict:
    body = _get(f"/file/detail/{recording_id}")
    return {
        "id": body.get("id"),
        "title": body.get("filename"),
        "duration_seconds": body.get("duration"),
        "recorded_at": _ms_to_iso(body.get("start_time")),
        "summary": body.get("summary"),
    }


def get_transcript(recording_id: str) -> dict:
    body = _get(f"/file/detail/{recording_id}")
    return {
        "id": body.get("id"),
        "title": body.get("filename"),
        "duration_seconds": body.get("duration"),
        "recorded_at": _ms_to_iso(body.get("start_time")),
        "transcript": body.get("transcript"),
    }


def get_audio_url(recording_id: str) -> dict:
    body = _get(f"/file/temp-url/{recording_id}", params={"is_opus": "false"})
    return {
        "recording_id": recording_id,
        "url": body.get("url") or body.get("data"),
    }


def get_user_info() -> dict:
    body = _get("/user/me")
    return {
        "id": body.get("id"),
        "name": body.get("nickname"),
        "email": body.get("email"),
        "country": body.get("country"),
        "membership": body.get("membership_type"),
    }
