import requests
#from config import Config
from ..Service.TempPref import compare

def processBedroom(data):
   
        temperature=data.get('tempCapteur',0)
        humidity= data.get("humiditeCapteur",0)
        light= data.get("light",False)
        door= data.get("doorCapteur",False)
        gaz= data.get("gazCapteur",0)
        climatiseur= data.get("climatiseur",False)
        CurrentTime = data.get("timestamp",0)
        

        def SleepCheck():
                try:
                        CurrentHour = int(CurrentTime[11:13])  
                        if CurrentHour >=22 or CurrentHour < 6 :
                                if light == True:
                                        print("[SleepCheck] its time to sleep   -bedroom")
                                elif light == False and climatiseur == False:
                                        print("[SleepCheck] turn on the climatiseur with prefered temp")
                except Exception as e:
                        print(f"[SleepCheck] Error parsing timestamp: {e}")

        def verfiyTemp():
                compare(data)

        def MotionLight():      
                if door == True and light == False:
                        print("[MotionLight] Motion detected but light is off. Turning on the light in the bedroom.")        

        verfiyTemp() 
        #SleepCheck() 
        #MotionLight()
        return   