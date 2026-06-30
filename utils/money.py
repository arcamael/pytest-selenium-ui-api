"""Currency/amount parsing helpers.

Money is parsed to :class:`decimal.Decimal` (not float) so comparisons are exact
and tests need no tolerance/rounding.
"""

from __future__ import annotations

import re
from decimal import Decimal


def parse_money(text: str) -> Decimal:
    """Parse a monetary/label string into an exact ``Decimal``.

    Handles values like ``"€26.50"``, ``"Balance: €120.00"``, ``"Odds: 2.45"``.
    """
    match = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    if not match:
        raise ValueError(f"no numeric value found in {text!r}")
    return Decimal(match.group())


def decimal_from_float(value: float | int) -> Decimal:
    return Decimal(str(value))
