from typing import Literal
from alertable import Alertable, AssociatedSymbolsAlertable
from test_case import *
from ticker import Ticker


# 可以在此基础上进行任意的设计和修改
class TradeMonitor:
    def __init__(self):
        pass

    def _update_exchanges(self):
        exchanges = list[Exchange](Global_Data['exchanges'])
        for e in exchanges:
            symbols = list[Symbol](Global_Data['symbols'])
            symbols = [s for s in symbols if s.exchange_name == e.name]
            e.update_symbol(symbols)
        self.exchanges = {e.name: e for e in exchanges}
        
    def _update_groups(self):
        groups = list[Group](Global_Data['groups'])
        for g in groups:
            symbols = list[Symbol](Global_Data['symbols'])
            symbols = [s for s in symbols if s.group_name == g.name]
            g.update_symbol(symbols)
        self.groups = {g.name: g for g in groups}
        
    def _update_symbols(self):
        symbols = list[Symbol](Global_Data['symbols'])
        for s in symbols:
            s.update_group(self.groups[s.group_name])
            s.update_exchange(self.exchanges[s.exchange_name])
        self.symbols = {s.name: s for s in symbols}

    def on_trade(self, trade: dict):
        self._update_exchanges()
        self._update_groups()
        self._update_symbols()
        
        symbol_name = str(trade['name'])
        if symbol_name not in self.symbols:
            print(f"Symbol {symbol_name} not found")
            return
        symbol = self.symbols[symbol_name]
        time = int(trade['time'])
        quantity = int(trade['quantity'])
        side = str(trade['side'])
        price = float(trade['price'])
        ticker = Ticker(time, side, quantity, price)

        self.quantity_alerts_set: set[Alertable] = set()
        self.quantity_alerts_needed: list[Alertable] = []
        self.delta_alerts_set: set[Alertable] = set()
        self.delta_alerts_needed: list[Alertable] = []
        
        symbol_quantity_alert = symbol.update_quantity(ticker)
        symbol_delta_alert = symbol.update_delta(ticker)
        if symbol_quantity_alert:
            self.quantity_alerts_needed.append(symbol)
        if symbol_delta_alert:
            self.delta_alerts_needed.append(symbol)

        exchange = symbol.exchange
        if exchange:
            self._check_mapped_alert(exchange, ticker)
        else:
            print(f"Exchange {symbol.exchange_name} not found")

        group = symbol.group
        if group:
            self._check_mapped_alert(group, ticker)
        else:
            print(f"Group {symbol.group_name} not found")

        for quantity_alert in self.quantity_alerts_needed:
            quantity_alert.quantity_alert(ticker)
        for delta_alert in self.delta_alerts_needed:
            delta_alert.delta_alert(ticker)
    
    def _check_mapped_alert(self, alert: AssociatedSymbolsAlertable, ticker: Ticker):
        quantity_alert = alert.update_quantity(ticker)
        delta_alert = alert.update_delta(ticker)
        alerts = [alert]
        alerts.extend(alert.symbols)
        for alert in alerts:
            if quantity_alert:
                if alert not in self.quantity_alerts_set:
                    self.quantity_alerts_set.add(alert)
                    self.quantity_alerts_needed.append(alert)
            if delta_alert:
                if alert not in self.delta_alerts_set:
                    self.delta_alerts_set.add(alert)
                    self.delta_alerts_needed.append(alert)
                    
if __name__ == "__main__":
    monitor = TradeMonitor()

    print("-"*50)
    print("load_param_data1")
    load_param_data1()
    print("-"*50)
    print("load_trade_data1")
    load_trade_data1(monitor)
    
    print("-"*50)
    print("load_param_data2")
    load_param_data2()
    print("-"*50)
    print("load_trade_data2")
    load_trade_data2(monitor)
