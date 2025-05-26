from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Initialize with the stock ticker for KOSS
        self.ticker = "KOSS"
    
    @property
    def assets(self):
        # We're only interested in trading KOSS
        return [self.ticker]
    
    @property
    def interval(self):
        # Using 5-minute intervals for day trading analysis
        return "5min"
    
    def run(self, data):
        # Initialize allocation with no position
        allocation_dict = {self.ticker: 0}
        
        # Calculate RSI values for KOSS stock
        rsi_values = RSI(self.ticker, data["ohlcv"], length=14)  # Using the standard 14-period RSI
        
        if rsi_values is not None and len(rsi_values) > 0:
            current_rsi = rsi_values[-1]
            
            # Define RSI thresholds for oversold and overbought conditions
            oversold_threshold = 30
            overbought_threshold = 70
            
            # If RSI indicates the stock is oversold, allocate 100% to buying KOSS
            if current_rsi < oversold_threshold:
                log(f"RSI is {current_rsi}, which is below {oversold_threshold}. Buying KOSS.")
                allocation_dict[self.ticker] = 1
                
            # If RSI indicates the stock is overbought, sell any held KOSS stock
            elif current_rsi > overbought_threshold:
                log(f"RSI is {current_rsi}, which is above {overbought_threshold}. Selling KOSS.")
                allocation_dict[self.ticker] = 0  # Setting allocation to 0 simulates selling off
                
            # If RSI is between the overbought and oversold thresholds, maintain current position
            else:
                log(f"RSI is {current_rsi}, holding current position.")
                # The allocation remains as set at the start (either 0 or what was previously set)
                
        else:
            log("No RSI data available to make a decision.")
        
        return TargetAllocation(allocation_dict)