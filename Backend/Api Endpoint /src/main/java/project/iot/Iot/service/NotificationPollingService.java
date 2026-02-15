package project.iot.Iot.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import project.iot.Iot.model.Notification;
import project.iot.Iot.repository.NotificationRepository;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class NotificationPollingService {
    
    private final NotificationRepository notificationRepository;
    
    public void createNotification(String userEmail, String title, String body, String roomId, String alertType) {
        Notification notification = new Notification();
        notification.setUserEmail(userEmail);
        notification.setTitle(title);
        notification.setBody(body);
        notification.setRoomId(roomId);
        notification.setAlertType(alertType);
        notificationRepository.save(notification);
    }
    
    public List<Map<String, String>> getUnreadNotifications(String userEmail) {
        return notificationRepository.findByUserEmailAndReadFalse(userEmail)
            .stream()
            .map(n -> {
                Map<String, String> map = new HashMap<>();
                map.put("id", n.getId() != null ? n.getId() : "");
                map.put("title", n.getTitle() != null ? n.getTitle() : "Unknown");
                map.put("body", n.getBody() != null ? n.getBody() : "");
                map.put("roomId", n.getRoomId() != null ? n.getRoomId() : "");
                map.put("alertType", n.getAlertType() != null ? n.getAlertType() : "");
                map.put("createdAt", n.getCreatedAt() != null ? n.getCreatedAt().toString() : "");
                return map;
            })
            .collect(Collectors.toList());
    }
    
    public void markAsRead(String notificationId) {
        notificationRepository.findById(notificationId).ifPresent(n -> {
            n.setRead(true);
            notificationRepository.save(n);
        });
    }
}