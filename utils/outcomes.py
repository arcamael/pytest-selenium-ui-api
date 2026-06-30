from __future__ import annotations

from enum import StrEnum


class Outcome(StrEnum):
    HOME = "HOME"
    DRAW = "DRAW"
    AWAY = "AWAY"

    @property
    def key(self) -> str:
        return self.value.lower()
