from typing import List, Dict
from price_listener import PriceListener
from execution import ExecutionClient
class LimitOrderAgent(PriceListener):
    def __init__(self, execution_client: ExecutionClient) -> None:
        """
        :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
        """
        self.execution_client = execution_client
        self.orders: List[Dict] = []
        self.ibm_price_threshold = 100

    def on_price_tick(self, product_id: str, price: float):
        """
        Invoked on price updates; Executes orders if price meets the conditions.
        :param product_id: id of the product with updated price
        :param price: updated price of the product
        """
        # Check for the task 1 condition (buy 1000 shares of IBM if price < $100)
        if product_id == "IBM" and price < self.ibm_price_threshold:
            self.execution_client.buy(product_id, 1000)

        # Check for the limit order conditions and execute them if conditions are met
        for order in self.orders[:]:  # Copy to avoid modification during iteration
            if order["product_id"] == product_id:
                if (order["is_buy"] and price <= order["limit"]) or (not order["is_buy"] and price >= order["limit"]):
                    if order["is_buy"]:
                        self.execution_client.buy(product_id, order["amount"])
                    else:
                        self.execution_client.sell(product_id, order["amount"])
                    self.orders.remove(order)  # Remove the executed order

    def add_order(self, is_buy: bool, product_id: str, amount: int, limit: float):
        """
        Adds an order to buy/sell at a specific limit price.
        :param is_buy: True for buy, False for sell
        :param product_id: product identifier
        :param amount: amount to buy/sell
        :param limit: limit price to execute the order
        """
        order = {
            "is_buy": is_buy,
            "product_id": product_id,
            "amount": amount,
            "limit": limit
        }
        self.orders.append(order)
