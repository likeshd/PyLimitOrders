import unittest
from unittest.mock import Mock
from limit_order_agent import LimitOrderAgent
from execution import ExecutionException, ExecutionClient

class LimitOrderAgentTest(unittest.TestCase):
    def setUp(self):
        # Create a mock execution client
        self.mock_execution_client = Mock(spec=ExecutionClient)
        self.agent = LimitOrderAgent(self.mock_execution_client)

    def test_buy_1000_shares_ibm_when_price_below_100(self):
        # Test Task 1 - Buy 1000 shares of IBM when price is below $100
        self.agent.on_price_tick("IBM", 99)
        self.mock_execution_client.buy.assert_called_once_with("IBM", 1000)

    def test_add_order_and_execute(self):
        # Test adding a buy order and executing it when price drops to limit
        self.agent.add_order(True, "AAPL", 50, 150.0)  # Buy 50 shares at $150 or lower
        self.agent.on_price_tick("AAPL", 149.0)
        self.mock_execution_client.buy.assert_called_once_with("AAPL", 50)

    def test_add_order_and_execute_sell(self):
        # Test adding a sell order and executing it when price reaches the limit
        self.agent.add_order(False, "AAPL", 50, 200.0)  # Sell 50 shares at $200 or higher
        self.agent.on_price_tick("AAPL", 200.0)
        self.mock_execution_client.sell.assert_called_once_with("AAPL", 50)

    def test_order_not_executed_if_price_not_met(self):
        # Ensure that orders are not executed if the price doesn't meet the limit
        self.agent.add_order(True, "AAPL", 50, 150.0)  # Buy at $150
        self.agent.on_price_tick("AAPL", 151.0)
        self.mock_execution_client.buy.assert_not_called()

if __name__ == '__main__':
    unittest.main()
