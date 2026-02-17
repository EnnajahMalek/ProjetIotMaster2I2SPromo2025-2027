"""
Train Door Anomaly Detection Model

Reads training data from JSON file, trains model, saves to .pkl file
"""

import json
from pathlib import Path
from .anomaly_detector import DoorAnomalyDetector

# Paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "training_data.json"
MODEL_FILE = BASE_DIR / "models" / "door_anomaly.pkl"

def load_training_data():
    """Load training data from JSON file"""
    print(f"Loading training data from {DATA_FILE}...")
    
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Training data not found!\n"
            f"Please run: python mk/doorMonitoring/generate_data.py"
        )
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    print(f" Loaded {len(data)} records")
    return data

def filter_normal_data(data):
    """
    Filter only normal (non-anomaly) data for training
    
    Isolation Forest learns from NORMAL behavior,
    then flags deviations as anomalies
    """
    normal_data = [r for r in data if not r['is_anomaly']]
    anomaly_data = [r for r in data if r['is_anomaly']]
    
    print(f"\nDataset split:")
    print(f"  Normal samples: {len(normal_data)}")
    print(f"  Anomaly samples: {len(anomaly_data)}")
    
    return normal_data, anomaly_data

def train_model(normal_data):
    """Train the anomaly detector"""
    print("\n" + "="*60)
    print("TRAINING ANOMALY DETECTOR")
    print("="*60)
    
    detector = DoorAnomalyDetector(contamination=0.05)
    metrics = detector.train(normal_data)
    
    print("\nTraining Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    return detector

def test_model(detector, normal_data, anomaly_data):
    """Test the trained model"""
    print("\n" + "="*60)
    print("TESTING MODEL")
    print("="*60)
    
    # Test on normal data (should predict as normal)
    print("\nTesting on NORMAL samples (should predict as normal):")
    test_normal = normal_data[:20]  # First 20 normal samples
    
    normal_correct = 0
    for sample in test_normal:
        result = detector.predict(sample)
        if not result['is_anomaly']:
            normal_correct += 1
    
    print(f"  Correctly identified: {normal_correct}/{len(test_normal)} ({normal_correct/len(test_normal)*100:.1f}%)")
    
    # Test on anomaly data (should predict as anomaly)
    if anomaly_data:
        print("\nTesting on ANOMALY samples (should predict as anomaly):")
        test_anomaly = anomaly_data[:20]  # First 20 anomaly samples
        
        anomaly_correct = 0
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for sample in test_anomaly:
            result = detector.predict(sample)
            if result['is_anomaly']:
                anomaly_correct += 1
                severity_counts[result['severity']] += 1
        
        print(f"  Correctly identified: {anomaly_correct}/{len(test_anomaly)} ({anomaly_correct/len(test_anomaly)*100:.1f}%)")
        print(f"\n  Severity breakdown:")
        for severity, count in severity_counts.items():
            print(f"    {severity}: {count}")
    
    # Show example predictions
    print("\n" + "="*60)
    print("EXAMPLE PREDICTIONS")
    print("="*60)
    
    print("\nExample 1: Normal evening (door closed, lights on)")
    normal_example = {
        "hour": 20,
        "day_of_week": 2,
        "is_weekend": False,
        "is_night": False,
        "door_open": False,
        "livingroom_light": True,
        "bedroom_light": False,
        "kitchen_light": True,
        "toilet_light": False,
        "other_rooms_lights_on": 1,
        "any_light_on": True
    }
    result = detector.predict(normal_example)
    print(f"  Prediction: {result}")
    
    print("\nExample 2: Anomaly (door open at 2 AM, all lights off)")
    anomaly_example = {
        "hour": 2,
        "day_of_week": 2,
        "is_weekend": False,
        "is_night": True,
        "door_open": True,
        "livingroom_light": False,
        "bedroom_light": False,
        "kitchen_light": False,
        "toilet_light": False,
        "other_rooms_lights_on": 0,
        "any_light_on": False
    }
    result = detector.predict(anomaly_example)
    print(f"  Prediction: {result}")

def save_model(detector):
    """Save trained model to file"""
    print("\n" + "="*60)
    print("SAVING MODEL")
    print("="*60)
    
    detector.save_model(MODEL_FILE)

if __name__ == "__main__":
    print("="*60)
    print("DOOR MONITORING - MODEL TRAINING")
    print("="*60)
    
    # Step 1: Load data
    data = load_training_data()
    
    # Step 2: Split normal/anomaly data
    normal_data, anomaly_data = filter_normal_data(data)
    
    if len(normal_data) < 100:
        print(f"\n❌ ERROR: Not enough normal data!")
        print(f"   Need at least 100 samples, have {len(normal_data)}")
        print(f"   Please run: python mk/doorMonitoring/generate_data.py")
        exit(1)
    
    # Step 3: Train model
    detector = train_model(normal_data)
    
    # Step 4: Test model
    test_model(detector, normal_data, anomaly_data)
    
    # Step 5: Save model
    save_model(detector)
    
    print("\n" + "="*60)
    print(" TRAINING COMPLETE!")
    print("="*60)
    print(f"\nTrained model saved to: {MODEL_FILE}")
    print("\nYou can now use this model in your main project!")