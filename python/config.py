# AI Model Parameters
LOOKBACK_PERIOD = 100  # Number of candles to look back for predictions
FEATURES = [
    'open', 'high', 'low', 'close', 'volume',
    'ma_fast', 'ma_med', 'ma_slow',
    'rsi', 'macd', 'macd_signal'
]

# Trading Parameters
STOP_LOSS_PIPS = 50
TAKE_PROFIT_PIPS = 100