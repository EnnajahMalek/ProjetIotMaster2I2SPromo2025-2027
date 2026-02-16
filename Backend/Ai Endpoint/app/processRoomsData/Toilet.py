import requests
from config import Config
import time
from datetime import datetime
from ..Service.TempPref import compare
from ..Service.AlertMaker import AlertMaker
from ..Service.Sender import Sender

# Module-level variable to persist state across function calls
toilet_memory = {"light_start_time": None}


def processToilet(data):

        sender=Sender()
        temperature=data.get('tempCapteur',0)
        humidity= data.get("humiditeCapteur",0)
        light= data.get("light",False)
        door= data.get("doorCapteur",False)
        gaz= data.get("gazCapteur",0)
        climatiseur= data.get("climatiseur",False)

        alert_maker = AlertMaker()
        
        def light_time(light):
         current_time = datetime.now()

        # If light is ON and door is CLOSED (assuming door=True means someone is inside)
         if light == True:
            # If we haven't started counting yet, start now
            if toilet_memory["light_start_time"] is None:
                toilet_memory["light_start_time"] = current_time
                #p = alert_maker.create_alert('toilet', {'is_anomaly': False, 'severity': 'NORMAL', 'value': 0}, "Light", data.get("timestamp",0), 0)
                #print(p)
            # Calculate how many seconds have passed
            elapsed = (current_time - toilet_memory["light_start_time"]).total_seconds()
            p = alert_maker.create_alert('toilet', {'is_anomaly': False, 'severity': 'NORMAL', 'value': elapsed}, "Light", data.get("timestamp",0), elapsed)
            # 5 minutes = 300 seconds
            if elapsed >= 300:
                      p = alert_maker.create_alert('toilet', {'is_anomaly': True, 'severity': 'HIGH', 'value': elapsed}, "Light", data.get("timestamp",0), elapsed)
                      sender.send(p)            
         else: 
            # If light is turned OFF, reset the timer
            if toilet_memory["light_start_time"] is not None:
                toilet_memory["light_start_time"] = None
                
        def verfiyTemp():
                compare(data)

        
        def MotionLight():
                if door == True and light == False:
                        print("[MotionLight] Motion detected but light is off. Turning on the light in the toilet.")


        verfiyTemp()     
        light_time(light)            
        #MotionLight()
        return    