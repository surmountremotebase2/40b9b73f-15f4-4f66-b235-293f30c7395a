from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD, ATR
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of tickers you are interested in.
        self.tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA"]

        # Initialize any data requirements.
        self.data_list = []

    @property
    def interval(self):
        # Daily data to avoid day trading
        return "1day"

    @property
    def assets(self):
        # Return the list of assets we are interested in
        return self.tickers

    @property
    def data(self):
        # Override to define required data sources, including technical indicators.
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        
        # Check each ticker for signals
        for ticker in self.tickers:
            # Calculate MACD for each ticker
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            
            # Calculate ATR for managing volatility risk
            atr_data = ATR(ticker, data["ohlcv"], length=14)
            
            # Set initial allocation to none (0%)
            allocation_dict[ticker] = 0
            
            if macd_data is not None and atr_data is not None:
                # Buy (allocate) if MACD is positive and ATR is within an acceptable range
                if macd_data["MACD"][-1] > macd_data["signal"][-1] and atr_data[-1] < max(atr_data) * 0.75:
                    allocation_dict[ticker] = 1 / len(self.tickers)
                # Sell or stay out (allocate 0%) if conditions are not met
                else:
                    allocation_dict[ticker] = 0

        # The sum of all allocations should not exceed 1, representing 100% of the capital
        return TargetAllocation(allocation_dict)