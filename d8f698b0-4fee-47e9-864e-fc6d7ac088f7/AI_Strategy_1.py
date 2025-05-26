from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA

class TradingStrategy(Strategy):
    def __init__(self):
        # Only interested in KOSS for this strategy
        self.tickers = ["KOSS"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Daily data
        return "1day"

    @property
    def data(self):
        # No additional data sources needed for this strategy
        return []

    def run(self, data):
        """
        Run the trading strategy to generate target allocations based on EMA crossovers.
        
        :param data: The market data including price information.
        :return: TargetAllocation with allocation for KOSS.
        """
        # Short-term and long-term EMA windows
        short_window = 12
        long_window = 26
        
        # Default allocation is to not hold the asset
        allocation_dict = {"KOSS": 0}
        
        # Check if we have enough data points
        if len(data["ohlcv"]) < long_window:
            # Not enough data to compute EMA
            return TargetAllocation(allocation_dict)

        # Compute short-term and long-term EMA
        short_ema = EMA("KOSS", data["ohlcv"], short_window)
        long_ema = EMA("KOSS", data["ohlcv"], long_window)
        
        if not short_ema or not long_ema:
            # In case we encounter any issues calculating EMA
            return TargetAllocation(allocation_dict)
        
        # Entry signal: Short-term EMA crosses above Long-term EMA
        if short_ema[-1] > long_ema[-1] and short_ema[-2] < long_ema[-2]:
            allocation_dict["KOSS"] = 1  # Allocate 100% to KOSS
        
        # Exit signal will naturally occur because we only enter long positions, there's no explicit sell signal other than not entering a position.

        return TargetAllocation(allocation_dict)