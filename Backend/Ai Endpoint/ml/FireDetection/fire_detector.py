"""
Fire Detection ML Model

Hybrid system combining ML anomaly detection with rule-based safety checks
"""

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

class FireDetector:
    """
    Hybrid fire detection system:
    1. ML-based anomaly detection
    2. Rule-based detection for known patterns
    """
    
    def __init__(self, contamination=0.03):
        """
        Args:
            contamination: Expected percentage of fires in data (default 3%)
        """
        self.ml_model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=150,
            max_samples='auto',
            n_jobs=-1
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_columns = None
        
        # Rule-based thresholds
        # Gas values in PPM: Safe 100-300, Anomaly 301-600, Critical 601+
        self.rules = {
            'critical_temp': 50,
            'high_gas': 600,        # ppm - anomaly threshold
            'critical_gas': 1000,   # ppm - critical fire threshold
            'low_humidity': 30,
        }
    
    def train(self, training_data):
        """
        Train the fire detector
        
        Args:
            training_data: List of dicts with sensor readings
        
        Returns:
            dict: Training metrics
        """
        print(f"\nTraining on {len(training_data)} samples...")
        
        # Filter only normal data
        normal_data = [r for r in training_data if not r['is_fire']]
        print(f"Using {len(normal_data)} normal samples for training")
        
        # Convert to feature matrix
        X = self._prepare_features(normal_data)
        
        # Store feature columns
        self.feature_columns = list(X.columns)
        
        print(f"Features: {self.feature_columns}")
        print(f"Feature matrix shape: {X.shape}")
        
        # Normalize features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.ml_model.fit(X_scaled)
        self.is_trained = True
        
        print(" ML training complete!")
        
        # Calculate metrics
        predictions = self.ml_model.predict(X_scaled)
        scores = self.ml_model.score_samples(X_scaled)
        
        metrics = {
            "total_samples": len(training_data),
            "normal_samples": len(normal_data),
            "fire_samples": len(training_data) - len(normal_data),
            "features_count": len(self.feature_columns),
            "anomalies_detected_in_normal": sum(predictions == -1),
            "avg_score": float(np.mean(scores)),
            "min_score": float(np.min(scores)),
            "max_score": float(np.max(scores))
        }
        
        return metrics
    
    def predict(self, sensor_data):
        """
        Detect if current sensor readings indicate fire
        
        Args:
            sensor_data: Dict with current sensor readings
        
        Returns:
            dict: Detection result
        """
        # Step 1: Rule-based detection
        rule_result = self._check_rules(sensor_data)
        
        # Step 2: ML-based detection
        ml_result = None
        if self.is_trained:
            ml_result = self._check_ml(sensor_data)
        
        # Combine results
        is_fire = False
        confidence = 0.0
        severity = "NORMAL"
        fire_type = None
        detection_method = None

        # Prefer ML confidence (abs score) if available because it reflects
        # how sure the model is (even when there's no fire). Fall back to rule confidence.
        if ml_result is not None:
            confidence = ml_result.get('confidence', 0.0)
        else:
            confidence = rule_result.get('confidence', 0.0)

        # Determine detection and severity
        if rule_result['is_fire']:
            is_fire = True
            # keep rule's severity and fire_type
            severity = rule_result['severity']
            fire_type = rule_result['fire_type']
            detection_method = "rule_based"

        if ml_result is not None and ml_result.get('is_fire'):
            is_fire = True
            # if rule also detected, mark hybrid and take max confidence
            if rule_result['is_fire']:
                confidence = max(confidence, ml_result.get('confidence', 0.0))
                detection_method = "hybrid"
            else:
                detection_method = "ml_based"
                # use ML severity when ML indicates fire
                severity = ml_result.get('severity', severity)
        
        return {
            "is_fire": is_fire,
            "confidence": round(confidence, 3),
            "severity": severity,
            "fire_type": fire_type,
            "detection_method": detection_method,
            "rule_check": rule_result,
            "ml_check": ml_result
        }
    
    def _check_rules(self, data):
        """Rule-based fire detection"""
        #  FIX 1: Handle both French and English field names, convert to float safely
        temp = data.get('tempCapteur') or data.get('temp') or 0
        gas = data.get('gazCapteur') or data.get('gas') or 0
        humidity = data.get('humiditeCapteur') or data.get('humidity') or 50
        
        # Convert to float (handles None, strings, etc.)
        try:
            temp = float(temp)
            gas = float(gas)
            humidity = float(humidity)
        except (ValueError, TypeError):
            temp = 0.0
            gas = 0.0
            humidity = 50.0
        
        is_fire = False
        confidence = 0.0
        severity = "NORMAL"
        fire_type = None
        triggers = []
        
        # Rule 1: Critical temperature
        if temp > self.rules['critical_temp']:
            is_fire = True
            confidence = min(1.0, (temp - self.rules['critical_temp']) / 30)
            triggers.append(f"temp_critical_{temp}C")
            severity = "CRITICAL" if temp > 60 else "HIGH"
        
        # Rule 2: High temp + high gas (anomaly level 301-600 ppm)
        if temp > 45 and gas > self.rules['high_gas']:
            is_fire = True
            confidence = 0.9
            fire_type = "gas_fire"
            triggers.append(f"high_temp_and_gas_{gas}ppm")
            severity = "CRITICAL"
        
        # Rule 3: High temp + low humidity
        if temp > 40 and humidity < self.rules['low_humidity']:
            is_fire = True
            confidence = 0.85
            fire_type = "electrical_or_smoldering"
            triggers.append("high_temp_low_humidity")
            severity = "HIGH"
        
        # Rule 4: Critical gas levels (601+ ppm)
        if gas > self.rules['critical_gas']:
            is_fire = True
            confidence = 0.95
            fire_type = "gas_fire"
            triggers.append(f"critical_gas_{gas}ppm")
            severity = "CRITICAL"
        
        return {
            "is_fire": is_fire,
            "confidence": confidence,
            "severity": severity,
            "fire_type": fire_type,
            "triggers": triggers,
            "gas_ppm": round(gas, 1)
        }
    
    def _check_ml(self, data):
        """ML-based anomaly detection"""
        if not self.is_trained:
            return None
        
        try:
            # Convert to feature vector
            X = self._prepare_features([data])
            X_scaled = self.scaler.transform(X)
            
            # FIX 2: Extract scalar values properly from numpy arrays
            prediction = int(self.ml_model.predict(X_scaled)[0])
            score = float(self.ml_model.score_samples(X_scaled)[0])
            
            is_fire = (prediction == -1)
            
            confidence = abs(score) 
            severity = self._calculate_severity(score, is_fire)
            
            return {
                "is_fire": is_fire,
                "anomaly_score": score,
                "confidence": confidence,
                "severity": severity
            }
        except Exception as e:
            print(f"Error in ML check: {e}")
            return None
    
    def _prepare_features(self, data):
        """Convert raw sensor data to feature matrix"""
        features = []
        
        for record in data:
            #  FIX 3: Handle both French and English field names, convert safely
            temp = record.get('tempCapteur') or record.get('temp') or 0
            humidity = record.get('humiditeCapteur') or record.get('humidity') or 50
            gas = record.get('gazCapteur') or record.get('gas') or 0
            
            # Convert to float safely
            try:
                temp = float(temp)
                humidity = float(humidity)
                gas = float(gas)
            except (ValueError, TypeError):
                temp = 0.0
                humidity = 50.0
                gas = 0.0
            
            #  FIX 4: Handle both 'id' (your database) and 'room' fields
            room = record.get('id') or record.get('room') or 'unknown'
            
            # Time features
            hour = int(record.get('hour', 0))
            day_of_week = int(record.get('day_of_week', 0))
            is_weekend = bool(record.get('is_weekend', False))
            
            # Derived features (updated for PPM gas scale)
            temp_very_high = 1 if temp > 40 else 0
            temp_high = 1 if temp > 30 else 0
            gas_present = 1 if gas > 50 else 0          # ppm baseline
            gas_high = 1 if gas > 300 else 0            # ppm anomaly threshold
            humidity_low = 1 if humidity < 35 else 0
            humidity_very_low = 1 if humidity < 25 else 0
            
            # Interaction features
            temp_gas_product = temp * gas
            #  FIX 5: Prevent division by zero
            temp_humidity_ratio = temp / humidity if humidity > 0 else 0
            
            feature_vector = {
                'temp': temp,
                'humidity': humidity,
                'gas': gas,
                'hour': hour,
                'day_of_week': day_of_week,
                'is_weekend': int(is_weekend),
                'is_kitchen': 1 if room == 'kitchen' else 0,
                'is_bedroom': 1 if room == 'bedroom' else 0,
                'is_livingroom': 1 if room == 'livingroom' else 0,
                'is_toilet': 1 if room == 'toilet' else 0,
                'temp_very_high': temp_very_high,
                'temp_high': temp_high,
                'gas_present': gas_present,
                'gas_high': gas_high,
                'humidity_low': humidity_low,
                'humidity_very_low': humidity_very_low,
                'temp_gas_product': temp_gas_product,
                'temp_humidity_ratio': temp_humidity_ratio,
            }
            
            features.append(feature_vector)
        
        df = pd.DataFrame(features)
        
        # Ensure column order matches training
        if self.feature_columns is not None:
            df = df[self.feature_columns]
        
        return df
    
    def _calculate_severity(self, score, is_fire):
        """Map anomaly score to severity level"""
        if not is_fire:
            return "NORMAL"
        
        if score < -0.4:
            return "CRITICAL"
        elif score < -0.3:
            return "HIGH"
        elif score < -0.2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def save_model(self, filepath):
        """Save trained model"""
        if not self.is_trained:
            raise ValueError("Cannot save untrained model!")
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        model_data = {
            'ml_model': self.ml_model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'rules': self.rules
        }
        
        joblib.dump(model_data, filepath)
        print(f" Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load trained model"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        
        self.ml_model = model_data['ml_model']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.rules = model_data['rules']
        self.is_trained = True
        
