package project.iot.Iot.service;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Service;

import com.google.firebase.messaging.FirebaseMessaging;
import com.google.firebase.messaging.FirebaseMessagingException;
import com.google.firebase.messaging.Message;
import com.google.firebase.messaging.Notification;

@Service
public class NotificationService {
    private final MongoTemplate sensorMongoTemplate;
    
    public NotificationService(@Qualifier("primaryMongoTemplate") MongoTemplate sensorMongoTemplate) {
        this.sensorMongoTemplate = sensorMongoTemplate;
    }
    public String sendNotification(String token, String title, String body) {
        Message message = Message.builder()
            .setNotification(Notification.builder()
                .setTitle(title)
                .setBody(body)
                .build())
            .setToken(token)
            .build();
        try {
            String response = FirebaseMessaging.getInstance().send(message);
            return "Successfully sent message: " + response;
        } catch (FirebaseMessagingException e) {
            e.printStackTrace();
            return "Error: " + e.getMessage();
        }
    }
    
    
    
}
