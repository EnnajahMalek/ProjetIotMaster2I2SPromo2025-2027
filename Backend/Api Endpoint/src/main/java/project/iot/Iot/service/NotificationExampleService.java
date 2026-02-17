package project.iot.Iot.service;

import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;
import project.iot.Iot.Helper.StateHelper;
import project.iot.Iot.model.Alert;
import project.iot.Iot.model.AlertType;
import project.iot.Iot.model.Severity;

@Service
@RequiredArgsConstructor
public class NotificationExampleService {
    
    @Qualifier("sensorMongoTemplate")
    private final MongoTemplate sensorMongoTemplate;
    
    private final NotificationPollingService notificationPollingService;

    public String messageAlert(String title, String topic, Alert alert, String timestamp) {
        StringBuilder body = new StringBuilder();
        if (alert.getIs_anomaly()) {
            body.append("ALERT!!! - In ").append(alert.getRoomId());
        } else {
            body.append("Notice - In ").append(alert.getRoomId());
        }
        body.append(" - ").append(alert.getType());
        body.append(" \n");
        body.append(alert.getSeverity());
        body.append(" \n");
        body.append(alert.getDescription());
        body.append(" \n");
        body.append(timestamp); 
        
        handleAlert(alert);
        
        String bodyString = body.toString();
        
        // ✅ ONLY SAVE TO DATABASE - No Firebase!
        notificationPollingService.createNotification(
            "user@123h.hm",
            title,
            bodyString,
            alert.getRoomId(),
            alert.getType().toString()
        );
        
        return "Notification added";
    }

    public void handleAlert(Alert alert) {
        StateHelper stateHelper = new StateHelper(sensorMongoTemplate);
        AlertType type = alert.getType();
        if(alert.getSeverity()!=Severity.NORMAL){
            switch (type) {
                case Climatiseur:
                    stateHelper.casClima(alert.getRoomId());
                    break;
                case Fire:
                    stateHelper.casFire(alert.getRoomId());
                    break;
                case Light:
                    stateHelper.casLight(alert.getRoomId());
                    break;
                case Gaz:
                    stateHelper.casGaz(alert.getRoomId());
                    break;
                default: 
                    break;
            }
        } else {
            switch (type) {
                case Climatiseur:
                    stateHelper.casClimaInverse(alert.getRoomId());
                    break;
                case Fire:
                    stateHelper.casFireInverse(alert.getRoomId());
                    break;
                case Light:
                    stateHelper.casLightInverse(alert.getRoomId());
                    break;
                case Gaz:
                    stateHelper.casGazInverse(alert.getRoomId());
                    break;
                default: 
                    break;
            } 
        }
    }
}