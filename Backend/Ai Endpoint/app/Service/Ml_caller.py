from ml.doorMonitoring.translator import IoTDataBridge
from ml.doorMonitoring.anomaly_detector import DoorAnomalyDetector

from ml.FireDetection.translator import FireTranslator
from ml.FireDetection.fire_detector import FireDetector

import pandas as pd
import joblib
from pathlib import Path

def FireDetection(data):
    fire_translator = FireTranslator()
    MODEL_PATH = 'ml/FireDetection/models/fire_detector.pkl'
    detector = FireDetector()
    detector.load_model(MODEL_PATH)
  
    result=detector.predict(data)
    return result


def DoorMonitoring(data):
     ml_features = IoTDataBridge.translate(data)

     detector = DoorAnomalyDetector()
     detector.load_model('ml/doorMonitoring/models/door_anomaly.pkl')

     result = detector.predict(ml_features)
     return result






