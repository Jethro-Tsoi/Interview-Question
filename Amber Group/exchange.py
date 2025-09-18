from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING

from alertable import AssociatedSymbolsAlertable
from ticker import Ticker

if TYPE_CHECKING:
    from symbol import Symbol

class Exchange(AssociatedSymbolsAlertable):
    def __init__(self, name: str, quantity_limit: int, quantity_interval: int, delta_limit: float, delta_interval: int):
        super().__init__("exchange", quantity_limit, quantity_interval, delta_limit, delta_interval)
        self.name = name
        
    def update_symbol(self, symbols: list[Symbol]):
        self.symbols = symbols

    # def update_quantity(self, ticker: Ticker) -> bool:
    #     return super().update_quantity(ticker)
    
    # def update_delta(self, ticker: Ticker) -> bool:
    #     return super().update_delta(ticker)