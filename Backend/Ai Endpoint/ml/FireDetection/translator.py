import pandas as pd
import numpy as np

class FireTranslator:
    def __init__(self):
        # Memory to calculate 'Speed of Change'
        self.prev_temp = None
        self.prev_gas = None

    def prepare_for_ml(self, raw_data):
        """
        Transforms raw sensor data into the 'Fire Feature Vector'.
        Input: {'temp': 25, 'gas': 0.02, 'humidity': 40, 'room': 'kitchen'}
        """
        print(f"\n--- [DEBUG] Processing Raw Data: {raw_data} ---")
        
        # 1. Extract raw values
        temp = float(raw_data.get('tempCapteur', 0))
        gas = float(raw_data.get('gazCapteur', 0))
        humidity = float(raw_data.get('humiditeCapteur', 0))
        room_name = raw_data.get('id', '') 
        
        # 2. Calculate "Speed" (Deltas)
        temp_rate = 0.0
        gas_rate = 0.0
        
        if self.prev_temp is not None:
            temp_rate = temp - self.prev_temp
            gas_rate = gas - self.prev_gas
            print(f"[DEBUG] Memory Found. Temp Change: {temp_rate:+.2f} | Gas Change: {gas_rate:+.4f}")
        else:
            print("[DEBUG] No previous state found. Initializing rates at 0.0")
            
        # Update memory for the next reading
        self.prev_temp = temp
        self.prev_gas = gas

        # 3. Create Interaction Features
        fire_index = temp / (humidity + 1)
        
        # 4. Final Feature Vector
        features = {
            'temp': temp,
            'gas': gas,
            'humidity': humidity,
            'temp_rate': temp_rate,
            'gas_rate': gas_rate,
            'fire_index': fire_index,
            'is_kitchen': 1 if raw_data.get('room') == 'kitchen' else 0
        }

        df = pd.DataFrame([features])
        
        # Log the final shape and a peek at the values
        print(f"[DEBUG] Feature Vector Created. Shape: {df.shape}")
        print(f"[DEBUG] Vector Values:\n{df.to_string(index=False)}")
        print("--- [DEBUG] End Processing ---\n")

        return df

# Example Usage to test the debug logs:
# translator = FireTranslator()
# translator.prepare_for_ml({'temp': 25, 'gas': 0.02, 'humidity': 40, 'room': 'kitchen'})
# translator.prepare_for_ml({'temp': 28, 'gas': 0.05, 'humidity': 38, 'room': 'kitchen'})