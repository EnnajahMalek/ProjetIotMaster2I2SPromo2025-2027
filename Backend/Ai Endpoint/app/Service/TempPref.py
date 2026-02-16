# compare temp to temp prefere 
import requests 
from config import Config 
from ..Service.AlertMaker import AlertMaker
from ..Service.Sender import Sender


def compare(data):
  alert_maker = AlertMaker()
  sender=Sender()

  current_temp = data.get("tempCapteur",0)
  temp_prefere = data.get("temperaturePrefere",0)

  if current_temp  > temp_prefere + 2 :
    p =alert_maker.create_alert(data.get("id","unknown"), {'is_anomaly': False, 'severity': 'LOW', 'value': current_temp}, "Climatiseur", data.get("timestamp",0), current_temp)
    #sender.send(p)
  elif current_temp ==temp_prefere :
    p =alert_maker.create_alert(data.get("id","unknown"), {'is_anomaly': False, 'severity': 'NORMAL', 'value': current_temp}, "Climatiseur", data.get("timestamp",0), 0 )
    
