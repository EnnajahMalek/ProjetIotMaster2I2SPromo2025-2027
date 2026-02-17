"""
Generate synthetic door training data

This simulates 30 days of realistic front door behavior and saves to JSON file.
No MongoDB needed - everything stored in files.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Output file path
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = DATA_DIR / "training_data.json"

def generate_door_training_data(days=30, samples_per_hour=12):
    """
    Generate realistic front door patterns
    
    Args:
        days: Number of days to simulate
        samples_per_hour: Sampling frequency (12 = every 5 minutes)
    
    Returns:
        list: Training records
    """
    print(f"Generating {days} days of door training data...")
    print(f"Sampling frequency: every {60/samples_per_hour:.0f} minutes")
    
    start_date = datetime.now() - timedelta(days=days)
    records = []
    
    total_samples = days * 24 * samples_per_hour
    
    for i in range(total_samples):
        # Calculate timestamp
        timestamp = start_date + timedelta(minutes=i * (60 / samples_per_hour))
        
        # Generate realistic state for this time
        record = generate_realistic_state(timestamp)
        records.append(record)
        
        # Progress indicator
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1}/{total_samples} samples...")
    
    print(f" Generated {len(records)} total samples")
    return records

def generate_realistic_state(timestamp):
    """
    Generate realistic door and light states based on time of day
    
    This simulates typical household behavior:
    - Morning: Door activity (leaving for work)
    - Daytime: Door mostly closed (everyone out)
    - Evening: Door activity (coming home), lights on
    - Night: Door closed, lights off
    """
    hour = timestamp.hour
    day_of_week = timestamp.weekday()
    is_weekend = day_of_week >= 5
    is_night = (hour >= 22 or hour <= 6)
    
    # === DETERMINE DOOR AND LIGHT STATUS ===
    
    # Morning routine (7-9 AM weekdays, 9-11 AM weekends)
    if not is_weekend and 7 <= hour < 9:
        door_open = random.random() < 0.40  # 30% chance - leaving for work
        livingroom_light = random.random() < 0.20
        bedroom_light = random.random() < 0.60
        kitchen_light = random.random() < 0.70
        toilet_light = random.random() < 0.40
    
    elif is_weekend and 9 <= hour < 11:
        door_open = random.random() < 0.25
        livingroom_light = random.random() < 0.40
        bedroom_light = random.random() < 0.50
        kitchen_light = random.random() < 0.60
        toilet_light = random.random() < 0.30
    
    # Daytime - everyone out (9 AM - 5 PM)
    elif 9 <= hour < 17:
        if is_weekend:
            door_open = random.random() < 0.20
            livingroom_light = random.random() < 0.30
            bedroom_light = random.random() < 0.20
            kitchen_light = random.random() < 0.40
            toilet_light = random.random() < 0.15
        else:
            door_open = random.random() < 0.15  # Rarely open
            livingroom_light = random.random() < 0.05
            bedroom_light = random.random() < 0.02
            kitchen_light = random.random() < 0.05
            toilet_light = random.random() < 0.02
    
    # Evening return (5-7 PM)
    elif 17 <= hour < 19:
        door_open = random.random() < 0.35  # Coming home
        livingroom_light = random.random() < 0.70
        bedroom_light = random.random() < 0.30
        kitchen_light = random.random() < 0.80
        toilet_light = random.random() < 0.20
    
    # Evening activity (7-10 PM)
    elif 19 <= hour < 22:
        door_open = random.random() < 0.15  # Door mostly closed
        livingroom_light = random.random() < 0.80
        bedroom_light = random.random() < 0.30
        kitchen_light = random.random() < 0.60
        toilet_light = random.random() < 0.20
    
    # Late evening (10-11 PM)
    elif 22 <= hour < 23:
        door_open = random.random() < 0.08  # Almost never open
        livingroom_light = random.random() < 0.50
        bedroom_light = random.random() < 0.40
        kitchen_light = random.random() < 0.20
        toilet_light = random.random() < 0.15
    
    # Night (11 PM - 6 AM) - sleeping
    else:
        door_open = random.random() < 0.03  # 1% - very rare
        livingroom_light = random.random() < 0.05
        bedroom_light = random.random() < 0.10
        kitchen_light = random.random() < 0.05
        toilet_light = random.random() < 0.03
    
    # === CALCULATE DERIVED FEATURES ===
    
    other_rooms_lights_on  = sum([bedroom_light, kitchen_light, toilet_light])
    any_light_on = (livingroom_light or bedroom_light or kitchen_light or toilet_light)
    
    # === BUILD RECORD ===
    
    record = {
        # Timestamp
        "timestamp": timestamp.isoformat(),
        
        # Time features
        "hour": hour,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        "is_night": is_night,
        
        # Front door (livingroom door)
        "door_open": door_open,
        "livingroom_light": livingroom_light,
        
        # Other rooms
        "bedroom_light": bedroom_light,
        "kitchen_light": kitchen_light,
        "toilet_light": toilet_light,
        
        # Derived features
        "other_rooms_lights_on": other_rooms_lights_on,
        "any_light_on": any_light_on,
        
        # Label (normal by default)
        "is_anomaly": False
    }
    
    return record

def inject_anomalies(records, percentage=0.05):
    """
    Inject anomalies into the dataset
    
    This teaches the model what ABNORMAL behavior looks like:
    - Door open late at night
    - Door open with all lights off
    - Door open when everyone appears to be sleeping
    
    Args:
        records: List of training records
        percentage: Percentage of data to convert to anomalies (default 5%)
    
    Returns:
        list: Records with anomalies injected
    """
    print(f"\nInjecting anomalies ({percentage*100}% of data)...")
    
    num_anomalies = int(len(records) * percentage)
    
    # Find indices of night-time records (only inject anomalies at night)
    night_indices = [i for i, r in enumerate(records) if r['is_night']]
    
    if len(night_indices) < num_anomalies:
        print(f"  Warning: Not enough night samples. Using all {len(night_indices)} night samples.")
        anomaly_indices = night_indices
    else:
        anomaly_indices = random.sample(night_indices, num_anomalies)
    
    for idx in anomaly_indices:
        anomaly_type = random.choice([
            'door_open_at_night',
            'door_open_no_lights',
            'door_open_all_sleeping'
        ])
        
        if anomaly_type == 'door_open_at_night':
            # Door open late at night - very unusual
            records[idx]['door_open'] = True
            records[idx]['livingroom_light'] = False
            records[idx]['is_anomaly'] = True
        
        elif anomaly_type == 'door_open_no_lights':
            # Door open with NO lights anywhere
            records[idx]['door_open'] = True
            records[idx]['livingroom_light'] = False
            records[idx]['bedroom_light'] = False
            records[idx]['kitchen_light'] = False
            records[idx]['toilet_light'] = False
            records[idx]['other_rooms_lights_on'] = 0
            records[idx]['any_light_on'] = False
            records[idx]['is_anomaly'] = True
        
        elif anomaly_type == 'door_open_all_sleeping':
            # Door open, everyone sleeping
            records[idx]['door_open'] = True
            records[idx]['livingroom_light'] = False
            records[idx]['bedroom_light'] = False
            records[idx]['other_rooms_lights_on'] = 0
            records[idx]['any_light_on'] = False
            records[idx]['is_anomaly'] = True
    
    anomaly_count = sum(1 for r in records if r['is_anomaly'])
    print(f" Injected {anomaly_count} anomalies")
    
    return records

def save_to_file(records, filepath):
    """
    Save training data to JSON file
    """
    # Create directory if it doesn't exist
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to file
    with open(filepath, 'w') as f:
        json.dump(records, f, indent=2)
    
    print(f"\n Saved {len(records)} records to {filepath}")
    
    # Print summary
    normal_count = sum(1 for r in records if not r['is_anomaly'])
    anomaly_count = sum(1 for r in records if r['is_anomaly'])
    
    print("\nDataset Summary:")
    print(f"  Total records: {len(records)}")
    print(f"  Normal samples: {normal_count} ({normal_count/len(records)*100:.1f}%)")
    print(f"  Anomaly samples: {anomaly_count} ({anomaly_count/len(records)*100:.1f}%)")

if __name__ == "__main__":
    print("="*60)
    print("DOOR MONITORING - TRAINING DATA GENERATOR")
    print("="*60)
    
    # Step 1: Generate normal data
    records = generate_door_training_data(days=30, samples_per_hour=12)
    
    # Step 2: Inject anomalies
    records = inject_anomalies(records, percentage=0.05)
    
    # Step 3: Save to file
    save_to_file(records, OUTPUT_FILE)
    
    print("\n" + "="*60)
    print(" DATA GENERATION COMPLETE!")
    print("="*60)
    print("\nNext step: python mk/doorMonitoring/train_model.py")