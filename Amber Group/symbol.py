from __future__ import annotations
from collections import deque
from typing import TYPE_CHECKING

from alertable import Alertable
from ticker import Ticker

if TYPE_CHECKING:
    from exchange import Exchange
    from group import Group

class Symbol(Alertable):
    def __init__(self, 
                 name: str,
                 exchange_name: str,
                 group_name: str | None = None,
                 quantity_limit: int | None = None,
                 quantity_interval: int | None = None,
                 delta_limit: float | None = None,
                 delta_interval: int | None = None
                 ):
        if not all([group_name, quantity_limit, quantity_interval, delta_limit, delta_interval]):
            raise ValueError("All parameters are required")

        super().__init__("symbol", quantity_limit, quantity_interval, delta_limit, delta_interval)
        self.name = name
        self.exchange_name = exchange_name
        self.group_name = group_name
        
    def update_group(self, group: Group):
        self.group = group
        
    def update_exchange(self, exchange: Exchange):
        self.exchange = exchange

    # def quantity_alert(self, ticker: Ticker):
    #     print(f"{self.alert_type} {self.name} quantity alert")
        
    # def delta_alert(self, ticker: Ticker):
    #     print(f"{self.alert_type} {self.name} delta alert")
        
