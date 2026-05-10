import logging
from datetime import datetime, timezone

import httpx

from .auth import BASE_URL, auth_headers, get_token

logger = logging.getLogger("plaud-mcp")

_AUTH_FAIL_BODY_STATUSES = {-3900, -3901, -401}
_AUTH_FAIL_HTTP_STATUSES = {401, 403}


def _data_payload(body: dict) -> dict | list | None:
    for key, value in body.items():
        if isinstance(value, list) and key.startswith("data_"):
            return value
    for key, value in body.items():
        if isinstance(value, dict) and key.startswith("data_"):
            return value
    legacy = body.get("data")
    if legacy is not None:
        return legacy
    return None


def _items(body: dict) -> list:
    payload = _data_payload(body)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("list", "items", "files", "recordings"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    return []


def _detail(body: dict) -> dict:
    payload = _data_payload(body)
    if isinstance(payload, dict):
        return payload
    return body


def _request(path: str, params: dict | None = None) -> tuple[int, dict]:
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
    return response.status_code, body


def _get(path: str, params: dict | None = None, _retried: bool = False) -> dict:
    http_status, body = _request(path, params)
    body_status = body.get("status")

    if body_status == 0:
        return body

    is_auth_fail = (
        http_status in _AUTH_FAIL_HTTP_STATUSES
        or body_status in _AUTH_FAIL_BODY_STATUSES
        or (body_status is None and "detail" in body)
    )

    if is_auth_fail and not _retried:
        logger.warning(
            "Plaud auth-fout (http=%s body.status=%s) — probeer hernieuwd inloggen",
            http_status, body_status,
        )
        try:
            get_token(force_refresh=True)
        except RuntimeError as exc:
            raise RuntimeError(_auth_error_message(path, http_status, body_status, body, exc)) from None
        return _get(path, params, _retried=True)

    if is_auth_fail:
        raise RuntimeError(_auth_error_message(path, http_status, body_status, body))

    raise RuntimeError(f"Plaud API fout op {path}: {body}")


def _auth_error_message(path: str, http_status: int, body_status: object, body: dict, exc: Exception | None = None) -> str:
    msg = body.get("msg") or body.get("message") or body.get("detail") or body
    suffix = f" ({exc})" if exc else ""
    if body_status == -3900:
        return (
            f"Plaud auth-fout op {path}: {msg}. "
            f"Controleer of PLAUD_USER_ID en PLAUD_DEVICE_ID correct in je config staan.{suffix}"
        )
    return (
        f"Plaud auth-fout op {path}: {msg}. "
        f"Vernieuw je PLAUD_TOKEN — log opnieuw in op web.plaud.ai en kopieer een verse token uit DevTools.{suffix}"
    )


def _ms_to_iso(ms: int | float | None) -> str | None:
    if not isinstance(ms, (int, float)):
        return None
    seconds = ms / 1000 if ms > 1e12 else ms
    return datetime.fromtimestamp(seconds, tz=timezone.utc).isoformat()


def _ms_to_seconds(ms: int | float | None) -> int | None:
    if not isinstance(ms, (int, float)):
        return None
    return int(ms // 1000)


def _format_recording(item: dict) -> dict:
    return {
        "id": item.get("id"),
        "title": item.get("filename"),
        "duration_seconds": _ms_to_seconds(item.get("duration")),
        "recorded_at": _ms_to_iso(item.get("start_time")),
        "has_summary": bool(item.get("is_summary")),
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
    return _items(body)


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
    item = _detail(_get(f"/file/detail/{recording_id}"))
    return {
        "id": item.get("id") or recording_id,
        "title": item.get("filename"),
        "duration_seconds": _ms_to_seconds(item.get("duration")),
        "recorded_at": _ms_to_iso(item.get("start_time")),
        "summary": item.get("summary"),
    }


def get_transcript(recording_id: str) -> dict:
    item = _detail(_get(f"/file/detail/{recording_id}"))
    return {
        "id": item.get("id") or recording_id,
        "title": item.get("filename"),
        "duration_seconds": _ms_to_seconds(item.get("duration")),
        "recorded_at": _ms_to_iso(item.get("start_time")),
        "transcript": item.get("transcript"),
    }


def get_audio_url(recording_id: str) -> dict:
    body = _get(f"/file/temp-url/{recording_id}", params={"is_opus": "false"})
    payload = _data_payload(body)
    if isinstance(payload, str):
        url = payload
    elif isinstance(payload, dict):
        url = payload.get("url") or payload.get("temp_url") or payload.get("download_url")
    else:
        url = None
    return {"recording_id": recording_id, "url": url}


def get_user_info() -> dict:
    body = _get("/user/me")
    user = body.get("data_user") or {}
    state = body.get("data_state") or {}
    return {
        "id": user.get("id"),
        "name": user.get("nickname"),
        "email": user.get("email"),
        "country": user.get("country"),
        "membership": state.get("membership_type") or state.get("membership_flag"),
    }
