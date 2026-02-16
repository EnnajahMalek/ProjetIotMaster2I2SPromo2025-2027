"""
Generate synthetic fire detection training data

Simulates normal household patterns vs. fire scenarios.
Uses: Temperature, Gas, Humidity only
"""

import json
import random
import math
from datetime import datetime, timedelta
from pathlib import Path

# Output file path
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_FILE = DATA_DIR / "training_data.json"

def generate_fire_training_data(days=30, samples_per_hour=12):
    """
    Generate realistic sensor patterns for fire detection
    
    Args:
        days: Number of days to simulate
        samples_per_hour: Sampling frequency (12 = every 5 minutes)
    
    Returns:
        list: Training records
    """
    print(f"Generating {days} days of fire detection training data...")
    print(f"Sampling frequency: every {60/samples_per_hour:.0f} minutes")
    
    start_date = datetime.now() - timedelta(days=days)
    records = []
    
    total_samples = days * 24 * samples_per_hour
    rooms = ['livingroom', 'kitchen', 'bedroom', 'toilet']
    
    for i in range(total_samples):
        # Calculate timestamp
        timestamp = start_date + timedelta(minutes=i * (60 / samples_per_hour))
        
        # Randomly select room for this sample
        room = random.choice(rooms)
        
        # Generate realistic state for this time and room
        record = generate_realistic_state(timestamp, room)
        records.append(record)
        
        # Progress indicator
        if (i + 1) % 1000 == 0:
            print(f"  Generated {i + 1}/{total_samples} samples...")
    
    print(f" Generated {len(records)} total samples")
    return records

def generate_realistic_state(timestamp, room):
    """
    Generate realistic sensor readings based on room and time
    """
    hour = timestamp.hour
    day_of_week = timestamp.weekday()
    is_weekend = day_of_week >= 5
    
    # === ROOM-SPECIFIC BASE VALUES ===
    
    if room == 'kitchen':
        base_temp = 24.0
        base_humidity = 50.0
        has_gas = True
    elif room == 'bedroom':
        base_temp = 22.0
        base_humidity = 45.0
        has_gas = False
    elif room == 'livingroom':
        base_temp = 23.0
        base_humidity = 48.0
        has_gas = False
    else:  # toilet
        base_temp = 21.0
        base_humidity = 60.0
        has_gas = False
    
    # === TIME-BASED VARIATIONS ===
    
    # Temperature follows daily cycle (peaks at 6 PM)
    daily_temp_variation = 2 * math.sin((hour - 6) * math.pi / 12)
    temp = base_temp + daily_temp_variation
    
    # Add random noise
    temp += random.gauss(0, 0.8)
    
    # Humidity (inversely correlated with temp)
    humidity = base_humidity - (temp - base_temp) * 0.3
    humidity += random.gauss(0, 3)
    humidity = max(20, min(85, humidity))
    
    # === GAS PATTERNS (Kitchen only during cooking) in PPM (parts per million) ===
    # Safe: 100-300 ppm, Anomaly: 301-600 ppm, Critical: 601+ ppm
    
    gas = 0.0
    if has_gas and room == 'kitchen':
        # Cooking times: 7-9 AM, 12-1 PM, 6-8 PM
        is_cooking_time = (
            (7 <= hour < 9) or 
            (12 <= hour < 13) or 
            (18 <= hour < 20)
        )
        
        if is_cooking_time:
            # Gas usage during cooking (150-250 ppm safe range)
            gas = random.uniform(150, 250) if random.random() < 0.5 else 0.0
            # Temperature higher during cooking
            temp += random.uniform(2, 6)
            # Humidity higher from steam
            humidity += random.uniform(5, 15)
            humidity = min(85, humidity)
        else:
            # Occasional small gas (pilot light, water heater) - baseline 50-100 ppm
            gas = random.uniform(50, 100) if random.random() < 0.05 else 0.0
    
    # === BUILD RECORD ===
    
    record = {
        # Metadata
        "timestamp": timestamp.isoformat(),
        "room": room,
        "hour": hour,
        "day_of_week": day_of_week,
        "is_weekend": is_weekend,
        
        # Sensor readings
        "temp": round(temp, 2),
        "humidity": round(humidity, 2),
        "gas": round(gas, 3),
        
        # Label (normal by default)
        "is_fire": False,
        "fire_type": None,
        "fire_stage": None
    }
    
    return record

def inject_fire_scenarios(records, percentage=0.03):
    """
    Inject realistic fire scenarios into the dataset
    
    Fire scenarios:
    1. Electrical fire (temp spike, no gas, humidity drops)
    2. Gas fire (temp spike, high gas, humidity drops)
    3. Cooking fire (temp spike, moderate gas, humidity variable)
    4. Smoldering fire (slow temp rise, no gas, humidity drops)
    
    Args:
        records: List of training records
        percentage: Percentage of data to convert to fire scenarios (default 3%)
    
    Returns:
        list: Records with fire scenarios injected
    """
    print(f"\nInjecting fire scenarios ({percentage*100}% of data)...")
    
    num_fires = int(len(records) * percentage)
    fire_indices = random.sample(range(len(records)), num_fires)
    
    fire_types = [
        'electrical_fire',
        'gas_fire',
        'cooking_fire',
        'smoldering_fire'
    ]
    
    for idx in fire_indices:
        fire_type = random.choice(fire_types)
        
        if fire_type == 'electrical_fire':
            # Electrical fire: Rapid temp spike, NO gas, humidity drops
            records[idx]['temp'] = random.uniform(40, 65)
            records[idx]['gas'] = 0.0
            records[idx]['humidity'] = random.uniform(20, 35)
            records[idx]['is_fire'] = True
            records[idx]['fire_type'] = 'electrical'
            records[idx]['fire_stage'] = random.choice(['early', 'developing', 'active'])
        
        elif fire_type == 'gas_fire':
            # Gas fire: High temp, HIGH gas (700-1500 ppm), humidity drops
            records[idx]['temp'] = random.uniform(45, 70)
            records[idx]['gas'] = random.uniform(700, 1500)
            records[idx]['humidity'] = random.uniform(15, 30)
            records[idx]['is_fire'] = True
            records[idx]['fire_type'] = 'gas'
            records[idx]['fire_stage'] = random.choice(['early', 'developing', 'active'])
        
        elif fire_type == 'cooking_fire':
            # Cooking fire: Moderate-high temp, moderate gas (400-650 ppm), variable humidity
            records[idx]['temp'] = random.uniform(50, 80)
            records[idx]['gas'] = random.uniform(400, 650)
            records[idx]['humidity'] = random.uniform(25, 45)
            records[idx]['is_fire'] = True
            records[idx]['fire_type'] = 'cooking'
            records[idx]['fire_stage'] = random.choice(['developing', 'active'])
        
        elif fire_type == 'smoldering_fire':
            # Smoldering fire: Slower temp rise, no gas, humidity drops
            records[idx]['temp'] = random.uniform(35, 50)
            records[idx]['gas'] = 0.0
            records[idx]['humidity'] = random.uniform(20, 35)
            records[idx]['is_fire'] = True
            records[idx]['fire_type'] = 'smoldering'
            records[idx]['fire_stage'] = 'early'
    
    fire_count = sum(1 for r in records if r['is_fire'])
    print(f" Injected {fire_count} fire scenarios")
    
    # Print breakdown by type
    type_counts = {}
    for r in records:
        if r['is_fire']:
            fire_type = r['fire_type']
            type_counts[fire_type] = type_counts.get(fire_type, 0) + 1
    
    print("\nFire scenario breakdown:")
    for fire_type, count in type_counts.items():
        print(f"  {fire_type}: {count}")
    
    return records

def add_fire_progression_sequences(records):
    """
    Add realistic fire progression sequences
    
    A real fire develops over time: early → developing → active
    """
    print("\nAdding fire progression sequences...")
    
    num_sequences = 20
    
    for _ in range(num_sequences):
        # Find a random starting point with enough space
        start_idx = random.randint(0, len(records) - 10)
        
        if start_idx + 10 < len(records):
            fire_type = random.choice(['electrical', 'gas', 'cooking'])
            
            # Stage 1: Early detection (first 2 records)
            for i in range(2):
                idx = start_idx + i
                records[idx]['temp'] += random.uniform(3, 8)
                records[idx]['humidity'] -= random.uniform(5, 10)
                if fire_type == 'gas':
                    records[idx]['gas'] = random.uniform(0.1, 0.3)
                records[idx]['is_fire'] = True
                records[idx]['fire_type'] = fire_type
                records[idx]['fire_stage'] = 'early'
            
            # Stage 2: Developing (next 3 records)
            for i in range(2, 5):
                idx = start_idx + i
                records[idx]['temp'] += random.uniform(10, 20)
                records[idx]['humidity'] -= random.uniform(10, 20)
                if fire_type == 'gas':
                    records[idx]['gas'] = random.uniform(0.4, 0.8)
                records[idx]['is_fire'] = True
                records[idx]['fire_type'] = fire_type
                records[idx]['fire_stage'] = 'developing'
            
            # Stage 3: Active fire (next 5 records)
            for i in range(5, 10):
                idx = start_idx + i
                records[idx]['temp'] += random.uniform(25, 45)
                records[idx]['humidity'] -= random.uniform(20, 35)
                if fire_type == 'gas':
                    records[idx]['gas'] = random.uniform(0.8, 2.0)
                records[idx]['is_fire'] = True
                records[idx]['fire_type'] = fire_type
                records[idx]['fire_stage'] = 'active'
    
    print(f" Added {num_sequences} fire progression sequences")
    return records

def save_to_file(records, filepath):
    """Save training data to JSON file"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(records, f, indent=2)
    
    print(f"\n Saved {len(records)} records to {filepath}")
    
    # Print summary
    normal_count = sum(1 for r in records if not r['is_fire'])
    fire_count = sum(1 for r in records if r['is_fire'])
    
    print("\nDataset Summary:")
    print(f"  Total records: {len(records)}")
    print(f"  Normal samples: {normal_count} ({normal_count/len(records)*100:.1f}%)")
    print(f"  Fire samples: {fire_count} ({fire_count/len(records)*100:.1f}%)")
    
    # Room distribution
    room_counts = {}
    for r in records:
        room = r['room']
        room_counts[room] = room_counts.get(room, 0) + 1
    
    print("\nRoom distribution:")
    for room, count in room_counts.items():
        print(f"  {room}: {count}")

if __name__ == "__main__":
    print("="*60)
    print("FIRE DETECTION - TRAINING DATA GENERATOR")
    print("="*60)
    
    # Step 1: Generate normal data
    records = generate_fire_training_data(days=30, samples_per_hour=12)
    
    # Step 2: Inject fire scenarios
    records = inject_fire_scenarios(records, percentage=0.03)
    
    # Step 3: Add fire progression sequences
    records = add_fire_progression_sequences(records)
    
    # Step 4: Save to file
    save_to_file(records, OUTPUT_FILE)
    
    print("\n" + "="*60)
    print(" DATA GENERATION COMPLETE!")
    print("="*60)
    print("\nNext step: python -m mk.fireDetection.train_model")