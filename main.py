from datetime import datetime, date, timedelta

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from numpy import _1D
from numpy._core.fromnumeric import _0D

APCA_API_KEY_ID = 'PK2SYQVGFILZ2FKEPXUS4YR63F'
APCA_API_SECRET_KEY = 'HAbqVp6Ee6WcnwFkVWzbA7mwEAGDVAstRsHWJZrnd3nF'

# Stocks for Market Analysis
symbols = ['AAPL', 'MSFT', 'NVDA', 'TSLA', 'AMZN']

lookback_date = (date.today() - timedelta(days=366))

# Initialize with your API keys
stock_client = StockHistoricalDataClient(APCA_API_KEY_ID, APCA_API_SECRET_KEY)

# Set request parameters for a stock ticker
request_params = StockBarsRequest(
    symbol_or_symbols=symbols,
    timeframe=TimeFrame.Day,
    start=lookback_date
)

# Fetch historical data
stock_bars = stock_client.get_stock_bars(request_params)
bars_df = stock_bars.df

# Moving average windows
ma_windows = [5,20,50,200]

# Get moving averages
for window in ma_windows:
    col_name = f"MA_{window}"
    bars_df[col_name] = (
        bars_df.groupby(level="symbol")["close"]
        .transform(lambda s: s.rolling(window).mean())
    )

# Get daily return
bars_df["daily_return"] = (
    bars_df.groupby(level="symbol")["close"]
    .transform(lambda s: s.pct_change())
)

# Calculate percentage
bars_df["daily_return_pct"] = bars_df["daily_return"] * 100

bars_df["RSI_14"] = (
    bars_df.groupby(level="symbol"["close"]
    .transform(lambda s: ta.rsi(s, length=14))
)

# VWAP Signals
bars_df["above_vwap"] = bars_df["close"] > bars_df["vwap"]

bars_df["vwap_signal"] = 0
bars_df.loc[bars_df["close"] > bars_df["vwap"], "vwap_signal"] = 1
bars_df.loc[bars_df["close"] < bars_df["vwap"], "vwap_signal"] = -1

# Relative Volume
bars_df["avg_volume_20"] = (
    bars_df.groupby(level="symbol")["volue"]
    .transform(lambda s: s.rolling(20).mean())
)

bars_df["relative_volume"] = bars_df["volume"] / bars_df["avg_volume_20"]

bars_df["volume_signal"] = 0
bars_df.loc[bars_df["relative_volume"] >= 1.5, "volume_signal"] = 1
bars_df.loc[bars_df["relative_volume"] <= 0.5, "volume_signal"] = -1

# Write to CSV
bars_df.to_csv("backtest_data.csv", index=True)


