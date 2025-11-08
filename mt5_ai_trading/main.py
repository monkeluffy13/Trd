import mt5_handler
import ai_model
import config
import time
from datetime import datetime

def main():
    # Initialize MT5 connection
    if not mt5_handler.initialize_mt5():
        print("Failed to initialize MT5")
        return
    
    print("MT5 initialized successfully")
    
    # Create AI model instance
    trading_ai = ai_model.TradingAI()
    
    # Initial training
    print("Getting historical data for initial training...")
    df = mt5_handler.get_historical_data(n_candles=2000)
    if df is None:
        print("Failed to get historical data")
        return
    
    # Calculate indicators
    df = mt5_handler.calculate_indicators(df)
    
    # Prepare and train model
    print("Training AI model...")
    X, y = trading_ai.prepare_data(df)
    trading_ai.train(X, y)
    print("Model training completed")
    
    # Main trading loop
    while True:
        try:
            # Get latest market data
            df = mt5_handler.get_historical_data(n_candles=config.LOOKBACK_PERIOD + 1)
            if df is None:
                print("Failed to get market data")
                time.sleep(60)
                continue
            
            # Calculate indicators
            df = mt5_handler.calculate_indicators(df)
            
            # Prepare features for prediction
            features = df[config.FEATURES].values[-config.LOOKBACK_PERIOD:]
            
            # Get AI prediction
            prediction = trading_ai.predict(features)
            
            # Get current market info
            symbol_info = mt5.symbol_info(config.MT5_SYMBOL)
            if symbol_info is None:
                print(f"Failed to get symbol info for {config.MT5_SYMBOL}")
                continue
                
            current_price = symbol_info.ask
            
            # Place trade based on AI prediction
            if prediction == 1:  # Up trend
                print(f"AI predicts UP trend for {config.MT5_SYMBOL}")
                sl, tp = mt5_handler.calculate_sl_tp(
                    current_price,
                    mt5.ORDER_TYPE_BUY,
                    config.STOP_LOSS_PIPS,
                    config.TAKE_PROFIT_PIPS,
                    symbol_info.point
                )
                mt5_handler.place_trade(
                    config.MT5_SYMBOL,
                    mt5.ORDER_TYPE_BUY,
                    config.LOT_SIZE,
                    current_price,
                    sl,
                    tp
                )
                
            elif prediction == 0:  # Down trend
                print(f"AI predicts DOWN trend for {config.MT5_SYMBOL}")
                sl, tp = mt5_handler.calculate_sl_tp(
                    current_price,
                    mt5.ORDER_TYPE_SELL,
                    config.STOP_LOSS_PIPS,
                    config.TAKE_PROFIT_PIPS,
                    symbol_info.point
                )
                mt5_handler.place_trade(
                    config.MT5_SYMBOL,
                    mt5.ORDER_TYPE_SELL,
                    config.LOT_SIZE,
                    current_price,
                    sl,
                    tp
                )
                
            else:  # Neutral
                print(f"AI predicts NEUTRAL trend for {config.MT5_SYMBOL}")
            
            # Wait before next iteration
            time.sleep(900)  # Wait 15 minutes (for M15 timeframe)
            
        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            time.sleep(60)
            
if __name__ == "__main__":
    main()