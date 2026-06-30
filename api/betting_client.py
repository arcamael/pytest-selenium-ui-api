"""
Thin HTTP client for the Sports Betting API.
"""

from __future__ import annotations

from typing import Any

import requests

from api.endpoints import Endpoint
from config import settings


class BettingClient:
    """Client for /api/matches, /api/balance, /api/place-bet, /api/reset-balance."""

    def __init__(
        self,
        base_url: str | None = None,
        user_id: str | None = None,
        timeout: int | None = None,
    ) -> None:
        # Resolve from settings at call time (not at def time) so per-test
        # overrides / monkeypatching of ``settings`` take effect.
        self.base_url = (base_url if base_url is not None else settings.API_BASE_URL).rstrip("/")
        self.user_id = user_id if user_id is not None else settings.USER_ID
        self.timeout = timeout if timeout is not None else settings.API_TIMEOUT
        self.session = requests.Session()

    # --- internals ----------------------------------------------------------
    def _headers(self, user_id: str | None) -> dict[str, str]:
        """Build request headers.

        ``user_id=None`` uses the client default; an empty string omits the
        header so callers can test the unauthorized path.
        """
        effective = self.user_id if user_id is None else user_id
        headers = {"Content-Type": "application/json"}
        if effective:
            headers["x-user-id"] = effective
        return headers

    def _request(
        self,
        method: str,
        path: Endpoint,
        *,
        user_id: str | None = None,
        json: Any = None,
    ) -> requests.Response:
        return self.session.request(
            method,
            f"{self.base_url}{path}",
            headers=self._headers(user_id),
            json=json,
            timeout=self.timeout,
        )

    # --- endpoints ----------------------------------------------------------
    def get_matches(self, user_id: str | None = None) -> requests.Response:
        """GET /api/matches — list of upcoming matches."""
        return self._request("GET", Endpoint.MATCHES, user_id=user_id)

    def get_balance(self, user_id: str | None = None) -> requests.Response:
        """GET /api/balance — current balance for the user."""
        return self._request("GET", Endpoint.BALANCE, user_id=user_id)

    def place_bet(
        self,
        match_id: str,
        selection: str,
        stake: Any,
        user_id: str | None = None,
    ) -> requests.Response:
        """POST /api/place-bet with a well-formed body.

        ``stake`` is intentionally typed ``Any`` so validation tests can send
        non-numeric or out-of-range values.
        """
        body = {"matchId": match_id, "selection": selection, "stake": stake}
        return self.place_bet_raw(body, user_id=user_id)

    def place_bet_raw(self, body: Any, user_id: str | None = None) -> requests.Response:
        """POST /api/place-bet with an arbitrary body.

        Escape hatch for malformed-payload / missing-field negative tests.
        """
        return self._request("POST", Endpoint.PLACE_BET, user_id=user_id, json=body)

    def reset_balance(self, user_id: str | None = None) -> requests.Response:
        """POST /api/reset-balance — restore the user's starting balance."""
        return self._request("POST", Endpoint.RESET_BALANCE, user_id=user_id)
