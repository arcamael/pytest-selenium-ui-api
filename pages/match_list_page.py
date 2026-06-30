from __future__ import annotations

from decimal import Decimal

from selenium.webdriver.common.by import By

from config import settings
from pages.base_page import BasePage
from utils.money import parse_money
from utils.outcomes import Outcome


class MatchListPage(BasePage):
    MATCH_LIST = (By.CSS_SELECTOR, ".matchList")
    MATCH_CARD = (By.CSS_SELECTOR, ".matchCard")
    HEADER_BALANCE = (By.ID, "header-balance")

    def load(self, user_id: str | None = None) -> MatchListPage:
        self.driver.get(settings.ui_url(user_id))
        self.find_visible(self.MATCH_CARD)
        return self

    def is_loaded(self) -> bool:
        return self.is_visible(self.MATCH_CARD)

    def odds_button(self, match_id: str, outcome: str | Outcome) -> tuple[str, str]:
        return (By.ID, f"odds-{match_id}-{Outcome(outcome).key}")

    def select_outcome(self, match_id: str, outcome: str | Outcome) -> None:
        self.click(self.odds_button(match_id, outcome))

    def header_balance_text(self) -> str:
        return self.text_of(self.HEADER_BALANCE)

    def header_balance(self) -> Decimal:
        return parse_money(self.header_balance_text())
