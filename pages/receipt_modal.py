from __future__ import annotations

from decimal import Decimal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.money import parse_money


class SuccessReceipt(BasePage):
    MODAL = (By.ID, "modal-success")
    BET_ID = (By.ID, "modal-success-bet-id")
    MATCH = (By.ID, "modal-success-match")
    STAKE = (By.ID, "modal-success-stake")
    ODDS = (By.ID, "modal-success-odds")
    PAYOUT = (By.ID, "modal-success-payout")
    PLACED_AT = (By.ID, "modal-success-placed-at")
    CLOSE_BTN = (By.ID, "modal-success-close")
    CLOSE_X_BTN = (By.ID, "modal-success-close-x")

    def wait_shown(self) -> SuccessReceipt:
        self.find_visible(self.MODAL)
        return self

    def is_shown(self) -> bool:
        return self.is_visible(self.MODAL)

    def body_text(self) -> str:
        """Full visible text of the modal (used to assert the Selection field)."""
        return self.text_of(self.MODAL)

    def bet_id(self) -> str:
        return self.text_of(self.BET_ID)

    def match(self) -> str:
        return self.text_of(self.MATCH)

    def stake(self) -> Decimal:
        return parse_money(self.text_of(self.STAKE))

    def odds(self) -> Decimal:
        return parse_money(self.text_of(self.ODDS))

    def payout_text(self) -> str:
        return self.text_of(self.PAYOUT)

    def payout(self) -> Decimal:
        return parse_money(self.payout_text())

    def placed_at(self) -> str:
        return self.text_of(self.PLACED_AT)

    def close(self) -> None:
        self.click(self.CLOSE_BTN)

    def wait_closed(self) -> None:
        self.wait_until_invisible(self.MODAL)
