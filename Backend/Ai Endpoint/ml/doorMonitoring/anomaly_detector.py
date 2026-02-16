"""
Door Anomaly Detector

ML model for detecting unusual door patterns
"""

from sklearn.ensemble import IsolationForest
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

class DoorAnomalyDetector:
    """
    Isolation Forest-based anomaly detector for door monitoring
    
    How it works:
    1. Train on normal door behavior
    2. Learn what's "typical" for each time of day
    3. Flag deviations as anomalies (potential forgotten door)
    """
    
    def __init__(self, contamination=0.05):
        """
        Args:
            contamination: Expected percentage of anomalies in data (default 5%)
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100,
            max_samples='auto',
            n_jobs=-1  # Use all CPU cores
        )
        self.is_trained = False
        self.feature_columns = None
    
    def train(self, training_data):
        """
        Train the anomaly detector
        
        Args:
            training_data: List of dicts with door/light features
        
        Returns:
            dict: Training metrics
        """
        print(f"\nTraining on {len(training_data)} samples...")
        
        # Convert to feature matrix
        X = self._prepare_features(training_data)
        
        # Store feature columns for consistency
        self.feature_columns = list(X.columns)
        
        print(f"Features: {self.feature_columns}")
        print(f"Feature matrix shape: {X.shape}")
        
        # Train model
        self.model.fit(X)
        self.is_trained = True
        
        print(" Training complete!")
        
        # Calculate training metrics
        predictions = self.model.predict(X)
        scores = self.model.score_samples(X)
        
        metrics = {
            "total_samples": len(training_data),
            "features_count": len(self.feature_columns),
            "anomalies_detected": sum(predictions == -1),
            "normal_detected": sum(predictions == 1),
            "avg_score": float(np.mean(scores)),
            "min_score": float(np.min(scores)),
            "max_score": float(np.max(scores))
        }
        
        return metrics
    
    def predict(self, sensor_data):
        """
        Predict if current door state is anomalous
        
        Args:
            sensor_data: Dict with current sensor readings
        
        Returns:
            dict: Prediction result
        """
        if not self.is_trained:
            raise ValueError("Model not trained yet!")
        
        # Convert to feature vector
        X = self._prepare_features([sensor_data])
        
        # Get prediction
        prediction = self.model.predict(X)[0]
        score = self.model.score_samples(X)[0]
        
        is_anomaly = (prediction == -1)
        
        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": float(score),
            "confidence": abs(float(score)),
            "severity": self._calculate_severity(score, is_anomaly)
        }
    
    def _prepare_features(self, data):
        """
        Convert raw data to feature matrix
        
        Features extracted:
        - Time: hour, day_of_week, is_weekend, is_night
        - Door/Lights: door_open, livingroom_light, bedroom_light, kitchen_light, toilet_light
        - Context: other_rooms_lights_on, any_light_on
        - Interactions: door_open_x_night, door_open_x_no_lights
        """
        features = []
        
        for record in data:
            feature_vector = {
                # Time features
                'hour': record['hour'],
                'day_of_week': record['day_of_week'],
                'is_weekend': int(record['is_weekend']),
                'is_night': int(record['is_night']),
                
                # Door and lights
                'door_open': int(record['door_open']),
                'livingroom_light': int(record['livingroom_light']),
                'bedroom_light': int(record['bedroom_light']),
                'kitchen_light': int(record['kitchen_light']),
                'toilet_light': int(record['toilet_light']),
                
                # Context
                'other_rooms_lights_on': record['other_rooms_lights_on'],
                'any_light_on': int(record['any_light_on']),
                
                # Interaction features (help model learn complex patterns)
                'door_open_x_night': int(record['door_open']) * int(record['is_night']),
                'door_open_x_no_lights': int(record['door_open']) * (1 - int(record['any_light_on'])),
            }
            
            features.append(feature_vector)
        
        df = pd.DataFrame(features)
        
        # Ensure column order matches training
        if self.feature_columns is not None:
            df = df[self.feature_columns]
        
        return df
    
    def _calculate_severity(self, score, is_anomaly):
        """
        Map anomaly score to severity level
        
        Isolation Forest scores are typically between -0.5 and 0.5
        More negative = more anomalous
        """
        if not is_anomaly:
            return "NORMAL"
        
        if score < -0.3:
            return "CRITICAL"
        elif score < -0.2:
            return "HIGH"
        elif score < -0.1:
            return "MEDIUM"
        else:
            return "LOW"
    
    def save_model(self, filepath):
        """Save trained model to file"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model!")
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(self.model, filepath)
        print(f" Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load trained model from file"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        self.model = joblib.load(filepath)
        self.is_trained = True
