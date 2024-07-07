from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import GDPAllCountries, InsiderTrading
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Trading only AAPL for simplicity
        self.tickers = ["AAPL"]
        # Instantiating GDP data
        self.data_list = [GDPAllCountries(), InsiderTrading("AAPL")]
    
    @property
    def interval(self):
        # Using 1 day interval for both the technical indicator and economic data
        return "1day"
    
    @property
    def assets(self):
        # Assets being considered in the strategy
        return self.tickers
    
    @property
    def data(self):
        # Data required for the strategy
        return self.data_list
    
    def run(self, data):
        # Default to no position
        allocation_dict = {"AAPL": 0}
        
        # Check the latest GDP data to ensure positive economic growth
        gdp_data = data[("gdp_by_country",)]
        if gdp_data and len(gdp_data) > 0:
            latest_gdp = gdp_data[-1]  # Assuming the latest data point is last in the list
            if latest_gdp["country"] == "United States" and latest_gdp["value"] > 0:
                # Economic condition is positive; now let's check the technical condition
                rsi = RSDOI("AAPL", data["ohlcv"], 14)  # 14-day RSI for AAPL
                if rsi and rsi[-1] < 30:
                    # RSI indicates AAPL is potentially oversold; setting buy allocation
                    allocation_dict["AAPL"] = 1  # Allocating fully into AAPL
                    
        # Return the target allocation based on the strategy's logic
        return TargetAllocation(allocation estion_dict)