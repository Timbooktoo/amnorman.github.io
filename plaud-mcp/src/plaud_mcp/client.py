import logging
from datetime import datetime, timezone

import httpx

from .auth import BASE_URL, auth_headers, get_token

logger = logging.getLogger("plaud-mcp")

_AUTH_FAIL_STATUSES = {-3900, -3901, -401, 401}


def _payload(body: dict) -> dict | list:
    data = body.get("data")
    return data if data is not None else body


def _items(body: dict) -> list:
    data = _payload(body)
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("list", "items", "files", "recordings"):
            value = data.get(key)
            if isinstance(value, list):
                return value
    return []


def _request(path: str, params: dict | None = None) -> dict:
    response = httpx.get(
        f"{BASE_URL}{path}",
        params=params,
        headers=auth_headers(),
        timeout=30,
    )
    try:
        body = response.json()
    except ValueError:
        logger.error(
            "Plaud GET %s gaf niet-JSON respons (HTTP %s): %s",
            path, response.status_code, response.text[:200],
        )
        response.raise_for_status()
        raise RuntimeError(f"Plaud API gaf onverwachte respons op {path}")

    logger.info(
        "Plaud GET %s -> HTTP %s body.status=%s body.keys=%s",
        path, response.status_code, body.get("status"), sorted(body.keys()),
    )
    return body


def _get(path: str, params: dict | None = None, _retried: bool = False) -> dict:
    body = _request(path, params)
    status = body.get("status")

    if status == 0 or status is None and "data" in body:
        return body

    if status in _AUTH_FAIL_STATUSES and not _retried:
        logger.warning(
            "Plaud auth-fout (status=%s msg=%s) — probeer hernieuwd inloggen",
            status, body.get("msg") or body.get("message"),
        )
        get_token(force_refresh=True)
        return _get(path, params, _retried=True)

    msg = body.get("msg") or body.get("message") or body
    if status == -3900:
        raise RuntimeError(
            f"Plaud auth-fout op {path}: {msg}. "
            f"Controleer of PLAUD_USER_ID en PLAUD_DEVICE_ID correct ingesteld zijn in .env."
        )
    raise RuntimeError(f"Plaud API fout op {path}: {body}")


def _ms_to_iso(ms: int | None) -> str | None:
    if ms is None or not isinstance(ms, (int, float)):
        return None
    if ms > 1e12:
        seconds = ms / 1000
    else:
        seconds = ms
    return datetime.fromtimestamp(seconds, tz=timezone.utc).isoformat()


def _format_recording(item: dict) -> dict:
    title = item.get("filename") or item.get("title") or item.get("name")
    started = item.get("start_time") or item.get("create_time") or item.get("created_at")
    return {
        "id": item.get("id") or item.get("file_id"),
        "title": title,
        "duration_seconds": item.get("duration"),
        "recorded_at": _ms_to_iso(started),
        "has_summary": bool(item.get("is_summary") or item.get("has_summary") or item.get("summary")),
        "keywords": item.get("keywords") or [],
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
    items = _items(body)
    if not items:
        logger.warning(
            "Plaud /file/simple/web gaf 0 items terug. body keys=%s data keys=%s",
            sorted(body.keys()),
            sorted(_payload(body).keys()) if isinstance(_payload(body), dict) else "n/a",
        )
    return items


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
        start = item.get("start_time") or item.get("create_time") or 0
        if from_ms <= start <= to_ms:
            results.append(_format_recording(item))
    return results


def search_recordings(query: str) -> list[dict]:
    q = query.lower()
    items = _fetch_all_recordings()
    results = []
    for item in items:
        title = (item.get("filename") or item.get("title") or item.get("name") or "").lower()
        keywords = [k.lower() for k in item.get("keywords") or []]
        if q in title or any(q in k for k in keywords):
            results.append(_format_recording(item))
    return results


def _detail_payload(body: dict) -> dict:
    data = _payload(body)
    return data if isinstance(data, dict) else body


def get_summary(recording_id: str) -> dict:
    item = _detail_payload(_get(f"/file/detail/{recording_id}"))
    return {
        "id": item.get("id") or item.get("file_id") or recording_id,
        "title": item.get("filename") or item.get("title"),
        "duration_seconds": item.get("duration"),
        "recorded_at": _ms_to_iso(item.get("start_time") or item.get("create_time")),
        "summary": item.get("summary"),
    }


def get_transcript(recording_id: str) -> dict:
    item = _detail_payload(_get(f"/file/detail/{recording_id}"))
    return {
        "id": item.get("id") or item.get("file_id") or recording_id,
        "title": item.get("filename") or item.get("title"),
        "duration_seconds": item.get("duration"),
        "recorded_at": _ms_to_iso(item.get("start_time") or item.get("create_time")),
        "transcript": item.get("transcript"),
    }


def get_audio_url(recording_id: str) -> dict:
    body = _get(f"/file/temp-url/{recording_id}", params={"is_opus": "false"})
    data = _payload(body)
    if isinstance(data, str):
        url = data
    elif isinstance(data, dict):
        url = data.get("url") or data.get("temp_url") or data.get("download_url")
    else:
        url = None
    return {"recording_id": recording_id, "url": url}


def get_user_info() -> dict:
    item = _detail_payload(_get("/user/me"))
    return {
        "id": item.get("id") or item.get("user_id"),
        "name": item.get("nickname") or item.get("name"),
        "email": item.get("email"),
        "country": item.get("country"),
        "membership": item.get("membership_type") or item.get("membership"),
    }
