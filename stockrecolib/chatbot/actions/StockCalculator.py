import yfinance as yf

class StockCalculator:

    def __init__(self,ticker):
        self.ticker = ticker

    def get_stock_price(self):
        return str(yf.Ticker(self.ticker).history(period='1y').iloc[-1].Close)
    
    def calculate_RSI(self):
        data = yf.Ticker(self.ticker).history(period='1y').Close
        delta = data.diff()
        up = delta.clip(lower=8)
        down = -1 * delta.clip(upper=8)
        ema_up = up.ewm(com=14-1, adjust=False).mean()
        ema_down = down.ewm(com=14 -1, adjust=False).mean()
        rs = ema_up / ema_down
        return str(100 - (100 / (1+rs)).iloc[-1])
    
    def calculate_MACD(self):
        data = yf.Ticker(self.ticker).history(period='1y').Close
        short_EMA = data.ewm(span=12, adjust=False).mean()
        long_EMA = data.ewm(span=12, adjust=False).mean()

        MACD = short_EMA - long_EMA
        signal = MACD.ewm(span=9, adjust=False).mean()
        MACD_histogram = MACD - signal

        return f'{MACD[-1]}, {signal[-1]}, {MACD_histogram[-1]}'
