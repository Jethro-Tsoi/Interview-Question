from abc import ABC, abstractmethod
from collections import deque

from ticker import Ticker

class Alertable:
    def __init__(self, alert_type: str, quantity_limit: int, quantity_interval: int, delta_limit: float, delta_interval: int):
        self.alert_type = alert_type
        self.quantity_limit = quantity_limit
        self.quantity_interval = quantity_interval
        self.delta_limit = delta_limit
        self.delta_interval = delta_interval
        self.quantity_sum = 0
        self.quantity_queue = deque()
        self.last_quantity_alert_time = -1
        self.delta_sum = 0.0
        self.delta_queue = deque()
        self.last_delta_alert_time = -1
        self.isPositiveDeltaAlert = False
    def quantity_alert(self, ticker: Ticker):
        print(f"{self.alert_type} {self.name} quantity alert")

    def delta_alert(self, ticker: Ticker):
        print(f"{self.alert_type} {self.name} {'positive' if self.isPositiveDeltaAlert else 'negative'} delta alert")

    def update_quantity(self, ticker: Ticker) -> bool:
        while self.quantity_queue and self.quantity_queue[0].time < ticker.time - self.quantity_interval:
            removed = self.quantity_queue.popleft()
            self.quantity_sum -= removed.quantity
        self.quantity_sum += ticker.quantity
        self.quantity_queue.append(ticker)
        if self.quantity_sum > self.quantity_limit:
            window_start = ticker.time - self.quantity_interval
            if self.last_quantity_alert_time < window_start:
                self.last_quantity_alert_time = ticker.time
                return True
        return False
    
    def update_delta(self, ticker: Ticker) -> bool:
        while self.delta_queue and self.delta_queue[0].time < ticker.time - self.delta_interval:
            removed = self.delta_queue.popleft()
            self.delta_sum -= removed.delta
        self.delta_sum += ticker.delta
        self.delta_queue.append(ticker)
        if abs(self.delta_sum) > self.delta_limit:
            self.isPositiveDeltaAlert = self.delta_sum > 0
            window_start = ticker.time - self.delta_interval
            if self.last_delta_alert_time < window_start:
                self.last_delta_alert_time = ticker.time
                return True
        return False
    
class AssociatedSymbolsAlertable(Alertable):
    def __init__(self, name: str, quantity_limit: int, quantity_interval: int, delta_limit: float, delta_interval: int):
        super().__init__(name, quantity_limit, quantity_interval, delta_limit, delta_interval)
        self.name = name
        self.symbols = []
        
    def update_delta(self, ticker: Ticker) -> bool:
        while self.delta_queue and self.delta_queue[0].time < ticker.time - self.delta_interval:
            removed = self.delta_queue.popleft()
            self.delta_sum -= removed.delta
        self.delta_sum += ticker.delta
        self.delta_queue.append(ticker)
        if abs(self.delta_sum) > self.delta_limit:
            isPositiveDeltaAlert = self.delta_sum > 0
            self.isPositiveDeltaAlert = isPositiveDeltaAlert
            for symbol in self.symbols:
                symbol.isPositiveDeltaAlert = isPositiveDeltaAlert
            window_start = ticker.time - self.delta_interval
            if self.last_delta_alert_time < window_start:
                self.last_delta_alert_time = ticker.time
                return True
        return False
