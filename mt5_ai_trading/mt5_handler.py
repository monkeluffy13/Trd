import MetaTrader5 as mt5
import pandas as pd
import numpy as np
from datetime import datetime
import config

def initialize_mt5():
    """Initialize connection to MetaTrader 5"""
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
        return False
    
    # Login to the trading account
    authorized = mt5.login(
        login=config.MT5_LOGIN,
        password=config.MT5_PASSWORD,
        server=config.MT5_SERVER
    )
    
    if not authorized:
        print(f"Login failed: {mt5.last_error()}")
        mt5.shutdown()
        return False
    
    return True

def get_historical_data(symbol=config.MT5_SYMBOL, timeframe=mt5.TIMEFRAME_M15, n_candles=1000):
    """Get historical price data from MT5"""
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)
    if rates is None:
        return None
    
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def calculate_indicators(df):
    """Calculate technical indicators"""
    # Moving averages
    df['ma_fast'] = df['close'].rolling(window=20).mean()
    df['ma_med'] = df['close'].rolling(window=50).mean()
    df['ma_slow'] = df['close'].rolling(window=200).mean()
    
    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = exp1 - exp2
    df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
    
    return df

def place_trade(symbol, order_type, lot_size, price, sl, tp):
    """Place a trade in MT5"""
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "magic": 234000,
        "comment": "AI Trading System",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Order failed: {result.comment}")
        return False
    
    return True

def calculate_sl_tp(entry_price, order_type, sl_pips, tp_pips, point):
    """Calculate Stop Loss and Take Profit levels"""
    if order_type == mt5.ORDER_TYPE_BUY:
        sl = entry_price - sl_pips * point
        tp = entry_price + tp_pips * point
    else:
        sl = entry_price + sl_pips * point
        tp = entry_price - tp_pips * point
    
    return sl, tp