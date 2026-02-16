import requests
from config import Config
from ..Service.Ml_caller import DoorMonitoring
from ..Service.TempPref import compare
from ..Service.AlertMaker import AlertMaker
from ..Service.Sender import Sender


def processLivingroom(data):
        alert_maker = AlertMaker()
        sender=Sender()
   
        temperature=data.get('tempCapteur',0)
        humidity= data.get("humiditeCapteur",0)
        light= data.get("light",False)
        door= data.get("doorCapteur",False)
        gaz= data.get("gazCapteur",0)
        climatiseur= data.get("climatiseur",False)
        CurrentTime = data.get("timestamp",0)
        


        #def DoorSecurity():
             #   if door == True and CurrentTime >= 22 or CurrentTime < 6:
            #            print("house door is open at (its night ) ")

           #     DoorSecurity()

       
         
    
        
        def  DoorSecurity():
                result = DoorMonitoring(data)
                p = alert_maker.create_alert('livingroom',result,"Door" ,data.get("timestamp",0), result.get('confidence',0.0))
                sender.send(p)
                              
        def verfiyTemp():
           compare(data)

        
        
        
        verfiyTemp()     
       
             
        DoorSecurity()
        return 
