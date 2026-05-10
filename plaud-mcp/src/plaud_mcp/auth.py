import base64
import json
import logging
import os
import time
import uuid
from pathlib import Path

import httpx

logger = logging.getLogger("plaud-mcp")

BASE_URL = "https://api.plaud.ai"
CONFIG_PATH = Path.home() / ".plaud" / "config.json"

DEFAULT_DEVICE_ID = "[object Object]"
DEFAULT_TIMEZONE = "Europe/Brussels"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

_cached_login_token: str | None = None


def _decode_jwt_exp(token: str) -> int | None:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload)).get("exp")
    except Exception:
        return None


def _load_cached_token() -> dict | None:
    if not CONFIG_PATH.exists():
        return None
    try:
        return json.loads(CONFIG_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def _save_token(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))


def _is_token_valid(token: str) -> bool:
    if not token:
        return False
    exp = _decode_jwt_exp(token)
    if exp is None:
        return True
    return exp > time.time() + 3600


def _login() -> str:
    email = os.environ.get("PLAUD_EMAIL")
    password = os.environ.get("PLAUD_PASSWORD")
    if not email or not password:
        raise RuntimeError(
            "Plaud token verlopen of ongeldig. Vernieuw PLAUD_TOKEN handmatig "
            "uit DevTools, of stel PLAUD_EMAIL+PLAUD_PASSWORD in voor automatisch hernieuwen."
        )

    response = httpx.post(
        f"{BASE_URL}/auth/access-token",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()

    access_token = body.get("access_token") or (body.get("data") or {}).get("access_token")
    if not access_token:
        raise RuntimeError(f"Login mislukt: {body}")

    _save_token({"access_token": access_token})
    logger.info("Plaud login succesvol — nieuwe token opgeslagen in %s", CONFIG_PATH)
    return access_token


def get_token(force_refresh: bool = False) -> str:
    global _cached_login_token

    if force_refresh:
        _cached_login_token = None
        token = _login()
        _cached_login_token = token
        return token

    env_token = os.environ.get("PLAUD_TOKEN")
    if env_token:
        if not _is_token_valid(env_token):
            logger.warning(
                "PLAUD_TOKEN env-var verloopt binnen 1 uur of is al verlopen — "
                "stel PLAUD_EMAIL+PLAUD_PASSWORD in voor automatisch hernieuwen."
            )
        return env_token

    if _cached_login_token and _is_token_valid(_cached_login_token):
        return _cached_login_token

    cached = _load_cached_token()
    if cached and _is_token_valid(cached.get("access_token", "")):
        _cached_login_token = cached["access_token"]
        return _cached_login_token

    token = _login()
    _cached_login_token = token
    return token


def auth_headers() -> dict:
    device_id = os.environ.get("PLAUD_DEVICE_ID", DEFAULT_DEVICE_ID)
    tz = os.environ.get("PLAUD_TIMEZONE", DEFAULT_TIMEZONE)
    headers = {
        "Authorization": f"Bearer {get_token()}",
        "x-device-id": device_id,
        "x-request-id": str(uuid.uuid4()),
        "origin": "https://web.plaud.ai",
        "referer": "https://web.plaud.ai/",
        "app-platform": "web",
        "app-language": "en",
        "timezone": tz,
        "accept-language": "en-US,en;q=0.9",
        "user-agent": DEFAULT_USER_AGENT,
    }
    user_id = os.environ.get("PLAUD_USER_ID")
    if user_id:
        headers["x-pld-user"] = user_id
    return headers
