from typing import Literal


class Ticker:
    def __init__(self, time: int, side: Literal['BUY', 'SELL'], quantity: int, price: float):
        self.time = time
        self.side = side == 'BUY'
        self.quantity = quantity
        self.price = price
        self.delta = quantity * price * (1 if self.side else -1)