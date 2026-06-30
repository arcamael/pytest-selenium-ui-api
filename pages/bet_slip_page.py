"""Bet slip panel (Feature Specification §2.2 / §2.3).

Right-side panel: shows the active selection, stake input, balance, computed
potential payout, and the Place Bet / Remove All actions. Locators use the
app's stable ``bet-slip-*`` ids.
"""

from __future__ import annotations

from decimal import Decimal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.money import parse_money


class BetSlipPage(BasePage):
    SLIP = (By.ID, "bet-slip")
    EMPTY = (By.CSS_SELECTOR, ".betSlipBodyEmpty")
    SELECTION_TEAMS = (By.CSS_SELECTOR, ".betSelectionTeams")
    SELECTION_MARKET = (By.CSS_SELECTOR, ".betSelectionMarket")
    SELECTION_ODDS = (By.CSS_SELECTOR, ".betSelectionOdds")
    STAKE_INPUT = (By.ID, "bet-slip-stake-input")
    TOTAL_STAKE = (By.ID, "bet-slip-total-stake")
    POTENTIAL_PAYOUT = (By.ID, "bet-slip-potential-payout")
    BALANCE = (By.ID, "bet-slip-balance")
    PLACE_BET_BTN = (By.ID, "bet-slip-place-bet")
    REMOVE_ALL_BTN = (By.ID, "bet-slip-remove-all")
    SELECTION_REMOVE_BTN = (By.ID, "bet-slip-selection-remove")

    # --- state --------------------------------------------------------------
    def has_selection(self) -> bool:
        return self.is_visible(self.SELECTION_TEAMS)

    def is_empty(self) -> bool:
        return self.is_visible(self.EMPTY)

    def selection_teams(self) -> str:
        return self.text_of(self.SELECTION_TEAMS)

    def selection_market(self) -> str:
        return self.text_of(self.SELECTION_MARKET)

    def selection_odds(self) -> Decimal:
        return parse_money(self.text_of(self.SELECTION_ODDS))

    def total_stake(self) -> Decimal:
        return parse_money(self.text_of(self.TOTAL_STAKE))

    def potential_payout_text(self) -> str:
        return self.text_of(self.POTENTIAL_PAYOUT)

    def potential_payout(self) -> Decimal:
        return parse_money(self.potential_payout_text())

    def balance_text(self) -> str:
        return self.text_of(self.BALANCE)

    def balance(self) -> Decimal:
        return parse_money(self.balance_text())

    def place_bet_enabled(self) -> bool:
        return self.is_enabled(self.PLACE_BET_BTN)

    # --- actions ------------------------------------------------------------
    def enter_stake(self, stake: Decimal | float | str) -> None:
        self.type_text(self.STAKE_INPUT, str(stake))

    def place_bet(self) -> None:
        self.click(self.PLACE_BET_BTN)

    def remove_all(self) -> None:
        self.click(self.REMOVE_ALL_BTN)
