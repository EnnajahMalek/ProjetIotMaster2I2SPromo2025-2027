"""
Train Fire Detection Model
"""

import json
from pathlib import Path
from fire_detector import FireDetector

# Paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "training_data.json"
MODEL_FILE = BASE_DIR / "models" / "fire_detector.pkl"

def load_training_data():
    """Load training data from JSON file"""
    print(f"Loading training data from {DATA_FILE}...")
    
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Training data not found!\n"
            f"Please run: python -m mk.fireDetection.generate_data"
        )
    
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    
    print(f" Loaded {len(data)} records")
    return data

def analyze_dataset(data):
    """Analyze dataset"""
    normal_data = [r for r in data if not r['is_fire']]
    fire_data = [r for r in data if r['is_fire']]
    
    print(f"\nDataset Analysis:")
    print(f"  Total samples: {len(data)}")
    print(f"  Normal samples: {len(normal_data)} ({len(normal_data)/len(data)*100:.1f}%)")
    print(f"  Fire samples: {len(fire_data)} ({len(fire_data)/len(data)*100:.1f}%)")
    
    if fire_data:
        fire_types = {}
        fire_stages = {}
        for r in fire_data:
            ftype = r.get('fire_type')
            fstage = r.get('fire_stage')
            if ftype:
                fire_types[ftype] = fire_types.get(ftype, 0) + 1
            if fstage:
                fire_stages[fstage] = fire_stages.get(fstage, 0) + 1
        
        print(f"\n  Fire type breakdown:")
        for ftype, count in fire_types.items():
            print(f"    {ftype}: {count}")
        
        print(f"\n  Fire stage breakdown:")
        for fstage, count in fire_stages.items():
            print(f"    {fstage}: {count}")
    
    return normal_data, fire_data

def train_model(data):
    """Train the fire detector"""
    print("\n" + "="*60)
    print("TRAINING FIRE DETECTOR")
    print("="*60)
    
    detector = FireDetector(contamination=0.03)
    metrics = detector.train(data)
    
    print("\nTraining Metrics:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    
    return detector

def test_model(detector, normal_data, fire_data):
    """Test the trained model"""
    print("\n" + "="*60)
    print("TESTING MODEL")
    print("="*60)
    
    # Test on normal data
    print("\n1. Testing on NORMAL samples:")
    
    test_normal = normal_data[:50]
    normal_correct = 0
    false_positives = 0
    
    for sample in test_normal:
        result = detector.predict(sample)
        if not result['is_fire']:
            normal_correct += 1
        else:
            false_positives += 1
    
    print(f"   Correctly identified as normal: {normal_correct}/{len(test_normal)} ({normal_correct/len(test_normal)*100:.1f}%)")
    print(f"   False positives: {false_positives}/{len(test_normal)} ({false_positives/len(test_normal)*100:.1f}%)")
    
    # Test on fire data
    if fire_data:
        print("\n2. Testing on FIRE samples:")
        
        test_fire = fire_data[:50] if len(fire_data) >= 50 else fire_data
        fire_detected = 0
        false_negatives = 0
        detection_methods = {}
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        
        for sample in test_fire:
            result = detector.predict(sample)
            if result['is_fire']:
                fire_detected += 1
                method = result['detection_method']
                if method:
                    detection_methods[method] = detection_methods.get(method, 0) + 1
                severity_counts[result['severity']] += 1
            else:
                false_negatives += 1
        
        print(f"   Correctly detected fires: {fire_detected}/{len(test_fire)} ({fire_detected/len(test_fire)*100:.1f}%)")
        print(f"   Missed fires: {false_negatives}/{len(test_fire)} ({false_negatives/len(test_fire)*100:.1f}%)")
        
        if detection_methods:
            print(f"\n   Detection method breakdown:")
            for method, count in detection_methods.items():
                print(f"     {method}: {count}")
        
        print(f"\n   Severity breakdown:")
        for severity, count in severity_counts.items():
            if count > 0:
                print(f"     {severity}: {count}")

def show_examples(detector):
    """Show example predictions"""
    print("\n" + "="*60)
    print("EXAMPLE PREDICTIONS")
    print("="*60)
    
    examples = [
        {
            "name": "Normal kitchen during cooking",
            "data": {"temp": 28, "humidity": 55, "gas": 0.15, "room": "kitchen", "hour": 18}
        },
        {
            "name": "Normal bedroom at night",
            "data": {"temp": 22, "humidity": 45, "gas": 0.0, "room": "bedroom", "hour": 23}
        },
        {
            "name": " Electrical fire",
            "data": {"temp": 55, "humidity": 25, "gas": 0.0, "room": "livingroom", "hour": 14}
        },
        {
            "name": " Gas fire",
            "data": {"temp": 60, "humidity": 28, "gas": 1.2, "room": "kitchen", "hour": 3}
        },
        {
            "name": " Smoldering fire",
            "data": {"temp": 38, "humidity": 30, "gas": 0.0, "room": "bedroom", "hour": 2}
        },
        {
            "name": " Cooking fire",
            "data": {"temp": 70, "humidity": 35, "gas": 0.5, "room": "kitchen", "hour": 19}
        }
    ]
    
    for example in examples:
        print(f"\n{example['name']}:")
        print(f"  Sensors: Temp={example['data']['temp']}°C, "
              f"Humidity={example['data']['humidity']}%, "
              f"Gas={example['data']['gas']}")
        
        result = detector.predict(example['data'])
        
        print(f"  Prediction: {' FIRE' if result['is_fire'] else ' Normal'}")
        print(f"  Confidence: {result['confidence']:.2f}")
        print(f"  Severity: {result['severity']}")
        if result['fire_type']:
            print(f"  Fire type: {result['fire_type']}")
        if result['detection_method']:
            print(f"  Method: {result['detection_method']}")

def save_model(detector):
    """Save model"""
    print("\n" + "="*60)
    print("SAVING MODEL")
    print("="*60)
    
    detector.save_model(MODEL_FILE)

if __name__ == "__main__":
    print("="*60)
    print("FIRE DETECTION - MODEL TRAINING")
    print("="*60)
    
    # Load data
    data = load_training_data()
    
    # Analyze
    normal_data, fire_data = analyze_dataset(data)
    
    if len(normal_data) < 100:
        print(f"\n ERROR: Not enough normal data!")
        exit(1)
    
    # Train
    detector = train_model(data)
    
    # Test
    test_model(detector, normal_data, fire_data)
    
    # Examples
    show_examples(detector)
    
    # Save
    save_model(detector)
    
    print("\n" + "="*60)
    print(" TRAINING COMPLETE!")
    print("="*60)
    print(f"\nModel saved to: {MODEL_FILE}")