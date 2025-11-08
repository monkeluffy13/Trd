import numpy as np
import pandas as pd
import json
import os
from ai_model import TradingAI

class MT5Interface:
    def __init__(self):
        self.ai_model = TradingAI()
        self.model_trained = False
        
    def prepare_data(self, data_json):
        """Convert JSON data from MT5 to pandas DataFrame"""
        try:
            # Parse JSON data
            data = json.loads(data_json)
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Calculate technical indicators
            self._calculate_indicators(df)
            
            return df
        except Exception as e:
            print(f"Error preparing data: {str(e)}")
            return None
    
    def _calculate_indicators(self, df):
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
    
    def train_model(self, data_json):
        """Train the AI model with historical data"""
        try:
            df = self.prepare_data(data_json)
            if df is None:
                return "Error preparing training data"
            
            X, y = self.ai_model.prepare_data(df)
            self.ai_model.train(X, y)
            self.model_trained = True
            
            return "Model trained successfully"
        except Exception as e:
            return f"Error training model: {str(e)}"
    
    def get_prediction(self, data_json):
        """Get trading prediction from the AI model"""
        try:
            if not self.model_trained:
                return json.dumps({"error": "Model not trained yet"})
            
            df = self.prepare_data(data_json)
            if df is None:
                return json.dumps({"error": "Error preparing data"})
            
            # Get latest features
            features = df[self.ai_model.features].values[-self.ai_model.lookback_period:]
            
            # Make prediction
            prediction = self.ai_model.predict(features)
            
            # Convert prediction to trading signal
            signal = {
                0: "SELL",
                1: "BUY",
                2: "NEUTRAL"
            }
            
            return json.dumps({
                "signal": signal[prediction],
                "confidence": float(prediction)
            })
            
        except Exception as e:
            return json.dumps({"error": f"Prediction error: {str(e)}"})