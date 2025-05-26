from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["KOSS"]
        self.data_list = []  # No specific external data required for this strategy
        self.trade_day_counter = 0

    @property
    def interval(self):
        """Use a daily interval for trading."""
        return "1day"

    @property
    def assets(self):
        """Operates on KOSS stock."""
        return self.tickers

    @property
    def data(self):
        """Returns the data list. No additional data required for this example."""
        return self.data_list

    def run(self, data):
        """Executes the trading strategy.

        Buys or sells 20% of the KOSS stock holdings every other day.
        """
        # Initialize KOSS stake at 0 for buying or selling decision
        koss_stake = 0
        
        # Check if trade_day_counter is odd or even to decide on buy/sell action
        if self.trade_day_counter % 2 == 0:
            # Buy day: allocate 20% of the portfolio to KOSS
            log("Buying 20% KOSS")
            koss_stake = 0.2
        else:
            # Sell day: reduce KOSS holding by 20%
            log("Selling 20% KOSS")
            koss_stake = -0.2  # Representing a sell as negative allocation for illustration
        
        # Increment the trade day counter after each run
        self.trade_day_counter += 1

        # Return the target allocation.
        # Note in a real scenario, managing the precise 20% buying or selling relative to existing portfolio may need more logic
        return TargetAllocation({"KOSS": koss_stake})