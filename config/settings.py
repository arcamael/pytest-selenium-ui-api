from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _env(name: str, default: str) -> str:
    value = os.getenv(name, "").strip()
    return value or default


# --- Application under test -------------------------------------------------
BASE_URL: str = _env("BASE_URL", "https://qae-assignment-tau.vercel.app").rstrip("/")
API_BASE_URL: str = f"{BASE_URL}/api"
USER_ID: str = _env("USER_ID", "")

# --- Browser ----------------------------------------------------------------
HEADLESS: bool = _env("HEADLESS", "true").lower() in {"1", "true", "yes"}
BROWSER_WINDOW_SIZE: str = _env("BROWSER_WINDOW_SIZE", "1920,1080")

# --- Timeouts (seconds) -----------------------------------------------------
DEFAULT_TIMEOUT: int = int(_env("DEFAULT_TIMEOUT", "10"))
API_TIMEOUT: int = int(_env("API_TIMEOUT", "15"))

# --- Business rules (Feature Specification §3) ------------------------------
STARTING_BALANCE: str = "120.00"
CURRENCY: str = "EUR"
STAKE_MIN: str = "1.00"
STAKE_MAX: str = "100.00"
STAKE_DECIMAL_PLACES: int = 2
ODDS_MIN: str = "1.01"
ODDS_MAX: str = "1000.00"


def require_user_id() -> str:
    """Return USER_ID or fail fast with setup guidance.

    Tests need an authenticating user-id; an empty value would otherwise
    surface as an opaque 401. Called by fixtures so the failure is actionable.
    """
    if not USER_ID:
        raise RuntimeError(
            "USER_ID is not set. Copy .env.example to .env and set USER_ID="
            "<your-user-id> (or export USER_ID=...). See README > Setup."
        )
    return USER_ID


def ui_url(user_id: str | None = None) -> str:
    return f"{BASE_URL}/?user-id={user_id or USER_ID}"
