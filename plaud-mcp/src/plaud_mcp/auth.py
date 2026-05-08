import json
import os
import time
from pathlib import Path

import httpx

BASE_URL = "https://api.plaud.ai"
CONFIG_PATH = Path.home() / ".plaud" / "config.json"
REFRESH_WINDOW_DAYS = 30


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


def _is_token_valid(token_data: dict) -> bool:
    if not token_data.get("access_token"):
        return False
    expires_at = token_data.get("expires_at", 0)
    refresh_threshold = time.time() + REFRESH_WINDOW_DAYS * 86400
    return expires_at > refresh_threshold


def _login() -> str:
    email = os.environ.get("PLAUD_EMAIL")
    password = os.environ.get("PLAUD_PASSWORD")
    if not email or not password:
        raise RuntimeError(
            "PLAUD_EMAIL en PLAUD_PASSWORD omgevingsvariabelen zijn vereist."
        )

    response = httpx.post(
        f"{BASE_URL}/auth/access-token",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    body = response.json()

    if body.get("status", -1) != 0 and "access_token" not in body:
        raise RuntimeError(f"Login mislukt: {body}")

    access_token = body.get("access_token")
    if not access_token:
        raise RuntimeError(f"Login gaf een leeg token terug: {body}")

    expires_at = time.time() + 300 * 86400
    _save_token({"access_token": access_token, "expires_at": expires_at})
    return access_token


def get_token() -> str:
    cached = _load_cached_token()
    if cached and _is_token_valid(cached):
        return cached["access_token"]
    return _login()


def auth_headers() -> dict:
    return {"Authorization": f"Bearer {get_token()}"}
