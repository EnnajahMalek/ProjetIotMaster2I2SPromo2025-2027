import requests
from config import Config
from app.processRoomsData.Livingroom import processLivingroom
from app.processRoomsData.Bedroom import processBedroom
from app.processRoomsData.Kitchen import processKitchen
from app.processRoomsData.Toilet import processToilet

def process(raw_data):
    currentRoom = raw_data['id']
    if currentRoom == "livingroom":
        processLivingroom(raw_data)
    elif currentRoom == "bedroom":
        processBedroom(raw_data)
    elif currentRoom == "kitchen":
        processKitchen(raw_data)
    elif currentRoom == "toilet":
        processToilet(raw_data)


    return raw_data