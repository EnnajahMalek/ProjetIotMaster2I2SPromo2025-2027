import requests
from config import Config
import joblib
from pathlib import Path
from ..Service.TempPref import compare
from ..Service.AlertMaker import AlertMaker

from ..Service.Ml_caller import FireDetection
from ..Service.Sender import Sender
# 1. INITIALIZE & LOAD MODEL (Do this once at the top)
# Create a detector instance and load the trained .pkl data
#from Service.Sender import Send

def processKitchen(data):
        sender=Sender()
        
        temperature=data.get('tempCapteur',0)
        humidity= data.get("humiditeCapteur",0)
        light= data.get("light",False)
        door= data.get("doorCapteur",False)
        gaz= data.get("gazCapteur",0)
        climatiseur= data.get("climatiseur",False)


        alert_maker = AlertMaker()

        def gazLeak():
            # Gas levels: 100-300 safe, 301-600 anomaly, 601+ critical
            try:
                gaz_level = float(gaz) if gaz is not None else 0.0
            except (TypeError, ValueError):
                gaz_level = 0.0

            if gaz_level >= 601:
                p = alert_maker.create_alert('kitchen', {'is_anomaly': True, 'severity': 'CRITICAL', 'value': gaz_level}, "Gaz", data.get("timestamp",0), gaz_level)
            elif gaz_level >= 301:
                p = alert_maker.create_alert('kitchen', {'is_anomaly': True, 'severity': 'HIGH', 'value': gaz_level}, "Gaz", data.get("timestamp",0), gaz_level)

            elif gaz_level >= 100:
                p = alert_maker.create_alert('kitchen', {'is_anomaly': True, 'severity': 'MEDUIM', 'value': gaz_level}, "Gaz", data.get("timestamp",0), gaz_level)
            else:
                p = alert_maker.create_alert('kitchen', {'is_anomaly': False, 'severity': 'NORMAL', 'value': gaz_level}, "Gaz", data.get("timestamp",0), gaz_level)
            #print(p)    
            sender.send(p)
             
           
        #def OnFire():
         #   if temperature > 50 and gaz > 0:
          #      print("fire detected in the kitchen !!!!!    / call police ")
        def isFire(data):
            try:
                data['room'] = 'kitchen'
                result = FireDetection(data)
                p = alert_maker.create_alert('kitchen', result, "Fire", data.get("timestamp", 0), data.get('tempCapteur', 0))
                sender.send(p)
            except Exception as e:
                print(f"[ERROR] isFire: {e}")


        
        def verfiyTemp():
                compare(data)
        
        
        verfiyTemp()     
        gazLeak()
        isFire(data)
        return