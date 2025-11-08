import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler
import config

class TradingAI:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        
    def prepare_data(self, df):
        """Prepare data for AI model"""
        # Drop any NaN values
        df = df.dropna()
        
        # Create features array
        features = df[config.FEATURES].values
        
        # Scale features
        features_scaled = self.scaler.fit_transform(features)
        
        # Create sequences for LSTM
        X, y = [], []
        for i in range(config.LOOKBACK_PERIOD, len(features_scaled)):
            X.append(features_scaled[i-config.LOOKBACK_PERIOD:i])
            # Create target: 1 for up trend, 0 for down trend, 2 for neutral
            price_change = df['close'].iloc[i] - df['close'].iloc[i-1]
            if price_change > 0:
                target = 1  # Up trend
            elif price_change < 0:
                target = 0  # Down trend
            else:
                target = 2  # Neutral
            y.append(target)
            
        return np.array(X), np.array(y)
    
    def build_model(self, input_shape):
        """Build and compile LSTM model"""
        model = Sequential([
            LSTM(50, input_shape=input_shape, return_sequences=True),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(3, activation='softmax')  # 3 classes: up, down, neutral
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        return model
    
    def train(self, X, y, epochs=50, batch_size=32, validation_split=0.2):
        """Train the model"""
        if self.model is None:
            self.build_model((X.shape[1], X.shape[2]))
            
        history = self.model.fit(
            X, y,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        return history
    
    def predict(self, features):
        """Make prediction for new data"""
        if self.model is None:
            raise Exception("Model not trained yet!")
            
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Reshape for LSTM
        features_reshaped = features_scaled.reshape((1, features_scaled.shape[0], features_scaled.shape[1]))
        
        # Get prediction probabilities
        prediction = self.model.predict(features_reshaped)
        
        # Get class with highest probability
        return np.argmax(prediction[0])