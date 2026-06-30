"""Readable assertions for API responses.

* `assert_success` — a request expected to succeed with a JSON *object* body.
  Reports if it was rejected instead, or if it succeeded with the wrong status,
  missing/unexpected fields, or wrong field values.
* `assert_success_list` — a request expected to succeed with a JSON *array* body
  (e.g. /matches). Reports if it was rejected instead, if the array is shorter than
  expected, or if any item has missing/unexpected fields.
* `assert_rejected` — a request expected to be rejected. Reports if it succeeded
  instead, or if it was rejected with the wrong envelope, error id, or message.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from typing import Any

import requests

from api.endpoints import Endpoint
from api.schemas import ERROR_ENVELOPE_FIELDS, SUCCESS_FIELDS, ErrorCode


def _body(response: requests.Response) -> str:
    """Pretty-printed JSON body, falling back to raw text for non-JSON."""
    try:
        return json.dumps(response.json(), indent=2, sort_keys=True)
    except ValueError:
        return response.text


def _json_object(response: requests.Response) -> dict[str, Any] | None:
    """The body as a dict, or ``None`` when it is not a JSON object."""
    try:
        parsed = response.json()
    except ValueError:
        return None
    return parsed if isinstance(parsed, dict) else None


def _json_list(response: requests.Response) -> list[Any] | None:
    """The body as a list, or ``None`` when it is not a JSON array."""
    try:
        parsed = response.json()
    except ValueError:
        return None
    return parsed if isinstance(parsed, list) else None


def _is_success_status(response: requests.Response) -> bool:
    return 200 <= response.status_code < 300


def _fields_for(endpoint: Endpoint) -> frozenset[str]:
    """The registered field set for an endpoint, or a clear error if unregistered."""
    try:
        return SUCCESS_FIELDS[endpoint]
    except KeyError:
        raise KeyError(f"No SUCCESS_FIELDS registered for {endpoint!r}; add it to api/schemas.py") from None


def _field_problems(actual: set[str], expected: set[str], prefix: str = "") -> list[str]:
    """Exact-set key diff as report lines: missing keys and unexpected extra keys."""
    problems: list[str] = []
    if missing := sorted(expected - actual):
        problems.append(f"{prefix}missing fields: {missing}")
    if unexpected := sorted(actual - expected):
        problems.append(f"{prefix}unexpected fields: {unexpected}")
    return problems


def _format(headline: str, expected: str, response: requests.Response) -> str:
    return f"{headline}\nExpected : {expected}\nActual   : HTTP {response.status_code}\nResponse :\n{_body(response)}"


def assert_success(
    response: requests.Response,
    *,
    endpoint: Endpoint | None = None,
    expected_status: int = 200,
    expected_fields: Iterable[str] | None = None,
    expected_values: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    # `endpoint` supplies the exact field set from the SUCCESS_FIELDS registry; an
    # explicit `expected_fields` overrides it for one-off cases.
    if expected_fields is None and endpoint is not None:
        expected_fields = _fields_for(endpoint)
    expected_values = expected_values or {}
    expected = f"success — HTTP {expected_status}"
    body = _json_object(response)

    # Expected success but the request was rejected.
    if body is not None and "error" in body:
        raise AssertionError(
            _format(
                f"Expected success but the request was rejected: "
                f"error={body.get('error')!r}, message={body.get('message')!r}.",
                expected,
                response,
            )
        )
    if not _is_success_status(response) or body is None:
        raise AssertionError(_format("Expected a successful JSON response.", expected, response))

    # Succeeded — collect every field/value/status discrepancy.
    problems: list[str] = []
    if response.status_code != expected_status:
        problems.append(f"status code: expected {expected_status}, got {response.status_code}")
    if expected_fields is not None:
        problems += _field_problems(set(body), set(expected_fields))
    for field, want in expected_values.items():
        if field not in body:
            problems.append(f"{field}: missing (expected {want!r})")
        elif body[field] != want:
            problems.append(f"{field}: expected {want!r}, got {body[field]!r}")
    if problems:
        raise AssertionError(
            _format("Succeeded but did not match expectations:\n  - " + "\n  - ".join(problems), expected, response)
        )
    return body


def assert_success_list(
    response: requests.Response,
    *,
    endpoint: Endpoint | None = None,
    expected_status: int = 200,
    item_fields: Iterable[str] | None = None,
    min_items: int = 1,
) -> list[dict[str, Any]]:
    """Assert the request succeeded with a JSON *array*, and return the parsed list.

    Reports, in order:

    1. **Got a failure** — the response is an error envelope (or a non-2xx status).
    2. **Succeeded, but wrong** — collects *all* discrepancies in one report:
       unexpected status code, too few items (``min_items``), and — per item — exact
       key-set mismatches against ``item_fields``.

    Like :func:`assert_success`, ``endpoint`` supplies ``item_fields`` from the
    ``SUCCESS_FIELDS`` registry (each item's expected key set); an explicit
    ``item_fields`` overrides it. Pass ``None`` for both to skip the per-item check.
    """
    if item_fields is None and endpoint is not None:
        item_fields = _fields_for(endpoint)
    expected = f"success — HTTP {expected_status}, JSON array of ≥{min_items} item(s)"

    # Expected success but the request was rejected.
    error_body = _json_object(response)
    if error_body is not None and "error" in error_body:
        raise AssertionError(
            _format(
                f"Expected success but the request was rejected: "
                f"error={error_body.get('error')!r}, message={error_body.get('message')!r}.",
                expected,
                response,
            )
        )
    body = _json_list(response)
    if not _is_success_status(response) or body is None:
        raise AssertionError(_format("Expected a successful JSON array.", expected, response))

    # Succeeded — collect every status/length/per-item discrepancy.
    problems: list[str] = []
    if response.status_code != expected_status:
        problems.append(f"status code: expected {expected_status}, got {response.status_code}")
    if len(body) < min_items:
        problems.append(f"item count: expected at least {min_items}, got {len(body)}")
    if item_fields is not None:
        expected_keys = set(item_fields)
        for i, item in enumerate(body):
            if not isinstance(item, dict):
                problems.append(f"item[{i}]: not a JSON object")
                continue
            problems += _field_problems(set(item), expected_keys, prefix=f"item[{i}] ")
    if problems:
        raise AssertionError(
            _format("Succeeded but did not match expectations:\n  - " + "\n  - ".join(problems), expected, response)
        )
    return body


def assert_rejected(
    response: requests.Response,
    *,
    expected_status: int,
    expected_error: ErrorCode,
) -> dict[str, Any]:
    expected = f"rejection — HTTP {expected_status}, error={expected_error.value!r} ({expected_error.message!r})"
    body = _json_object(response)

    # Expected rejection but the request succeeded.
    if _is_success_status(response) or body is None or "error" not in body:
        raise AssertionError(_format("Expected rejection but the request succeeded.", expected, response))

    # Rejected — collect every envelope/code/message discrepancy.
    problems: list[str] = []
    if response.status_code != expected_status:
        problems.append(f"status code: expected {expected_status}, got {response.status_code}")
    if set(body) != set(ERROR_ENVELOPE_FIELDS):
        problems.append(f"envelope keys: expected {set(ERROR_ENVELOPE_FIELDS)}, got {set(body)}")
    if body.get("error") != expected_error:
        problems.append(f"error code: expected {expected_error.value!r}, got {body.get('error')!r}")
    if body.get("message") != expected_error.message:
        problems.append(f"message: expected {expected_error.message!r}, got {body.get('message')!r}")
    if problems:
        raise AssertionError(
            _format("Rejected but did not match expectations:\n  - " + "\n  - ".join(problems), expected, response)
        )
    return body
