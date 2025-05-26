from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["KOSS"]  # Define the ticker we are interested in

    @property
    def interval(self):
        return "1day"  # Use daily data for analysis

    @property
    def assets(self):
        return self.tickers

    def run(self, data):
        allocation_dict = {}  # Initialize an empty allocation dictionary
        # Compute short-term (e.g., 10-day) and long-term (e.g., 30-day) SMAs
        short_sma = SMA("KOSS", data["ohlcv"], 10)
        long_sma = SMA("KOSS", data["ohlcv"], 30)

        if len(short_sma) > 0 and len(long_sma) > 0:  # Ensure the SMAs are available
            last_short_sma = short_sma[-1]
            last_long_sma = long_sma[-1]
            
            if last_short_sma > last_long_sma:
                # Short-term SMA crossed above the long-term SMA, indicating a buy signal
                log("Buying KOSS")
                allocation_dict["KOSS"] = 1.0  # Allocate 100% to KOSS
            elif last_short_sma < last_long_sma:
                # Short-term SMA crossed below the long-term SMA, indicating a sell signal
                log("Selling KOSS")
                allocation_dict["KOSS"] = 0  # Sell off KOSS (no allocation)
            else:
                # No clear signal, maintain previous allocation (can be adjusted to hold a position or not)
                log("No clear buy or sell signal for KOSS")
                allocation_dict["KOSS"] = 0.5  # Example placeholder, adjust based on strategy
        else:
            # In case SMAs are not available, no position is taken
            log("SMAs not available, taking no action for KOSS")
            allocation_dict["KOSS"] = 0

        return TargetAllocation(allocation_dict)