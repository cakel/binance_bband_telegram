# Author: Yogesh K for finxter.com
# python script: trading with Bollinger bands for Binance
from binance.client import Client
from binance.enums import HistoricalKlinesType
from _config import config
from _logger import logger
import pandas as pd     # needs pip install
import numpy as np
import matplotlib.pyplot as plt   # needs pip install
import pytz

client = Client(config["BINANCE_API_KEY"], config["BINANCE_API_SECRET_KEY"], testnet=False)
symbol = config["BINANCE_TRACE_SYMBOL"]
interval = config["BINANCE_TRACE_INTERVAL"]

def get_data_frame():
    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    # request historical candle (or klines) data using timestamp from above, interval either every min, hr, day or month
    # starttime = '30 minutes ago UTC' for last 30 mins time
    # e.g. client.get_historical_klines(symbol='ETHUSDTUSDT', '1m', starttime)
    # starttime = '1 Dec, 2017', '1 Jan, 2018'  for last month of 2017
    # e.g. client.get_historical_klines(symbol='BTCUSDT', '1h', "1 Dec, 2017", "1 Jan, 2018")

    starttime = '2 day ago UTC'  # to start for 1 day ago
    bars = client.get_historical_klines(symbol, interval, starttime, klines_type=HistoricalKlinesType.FUTURES)

    for line in bars:        # Keep only first 5 columns, "date" "open" "high" "low" "close"
        del line[5:]
    df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close']) #  2 dimensional tabular data

    return df
def plot_graph(df : pd.DataFrame):
    df=df.astype(float)
    df[['close', 'sma','upper', 'lower']].plot()
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Close/Last price',fontsize=18)
    x_axis = df.index
    plt.fill_between(x_axis, df['lower'], df['upper'], color='grey',alpha=0.30)
    plt.scatter(df.index,df['buy'], color='purple',label='Buy',  marker='^', alpha = 1) # purple = buy
    plt.scatter(df.index,df['sell'], color='red',label='Sell',  marker='v', alpha = 1)  # red = sell

    # plt.show()
    plt.savefig('output.jpg')
    plt.close()

def buy_or_sell(df):
    current_price = float(client.get_symbol_ticker(symbol =symbol)['price'])
    current_upper = pd.to_numeric(df.iloc[-1:]['upper'], downcast='float')[0]
    current_lower = pd.to_numeric(df.iloc[-1:]['lower'], downcast='float')[0]
    upper_lower_delta = current_upper - current_lower
    current_price_delta = current_price - current_lower
    current_price_percentage = current_price_delta / upper_lower_delta * 100.0

    logger.info(f"current_price: {current_price}, 15Min BBand Upper:{current_upper:.3f} Lower:{current_lower:.3f} => {current_price_percentage:.3f}%")
    return (current_price, current_upper, current_lower, current_price_percentage)

def bollinger_trade_logic():
    symbol_df = get_data_frame()
    period = 21
    # small time Moving average. calculate 21 moving average using Pandas over close price
    symbol_df['sma'] = symbol_df['close'].rolling(period).mean()
    # Get standard deviation
    symbol_df['std'] = symbol_df['close'].rolling(period).std()
    # Calculate Upper Bollinger band
    symbol_df['upper'] = symbol_df['sma']  + (2 * symbol_df['std'])
    # Calculate Lower Bollinger band
    symbol_df['lower'] = symbol_df['sma']  - (2 * symbol_df['std'])
    # To print in human readable date and time (from timestamp)
    symbol_df.set_index('date', inplace=True)
    symbol_df.index = pd.to_datetime(symbol_df.index, unit='ms') # index set to first column = date_and_time

    seoul = pytz.timezone('Asia/Seoul')
    symbol_df.index = symbol_df.index.tz_localize(pytz.utc).tz_convert(seoul)

    # prepare buy and sell signals. The lists prepared are still panda dataframes with float nos
    close_list = pd.to_numeric(symbol_df['close'], downcast='float')
    upper_list = pd.to_numeric(symbol_df['upper'], downcast='float')
    lower_list = pd.to_numeric(symbol_df['lower'], downcast='float')
    symbol_df['buy'] = np.where(close_list < lower_list,   symbol_df['close'], np.NaN )
    symbol_df['sell'] = np.where(close_list > upper_list,   symbol_df['close'], np.NaN )
    # with open('output.txt', 'w') as f:
    #     f.write(symbol_df.to_string())

    plot_graph(symbol_df)

    (current_price, current_upper, current_lower, current_price_percentage) = buy_or_sell(symbol_df)
    return (current_price, current_upper, current_lower, current_price_percentage)

if __name__ == "__main__":
    logger.warn("Use python main.py instead, Start collecting with default setting")
    bollinger_trade_logic()
       # Change symbol here e.g. BTCUSDT, BNBBTC, ETHUSDT, NEOBTC