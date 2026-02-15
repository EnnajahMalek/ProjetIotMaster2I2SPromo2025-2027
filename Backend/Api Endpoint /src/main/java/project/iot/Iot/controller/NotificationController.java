package project.iot.Iot.controller;
 
import java.util.List;
import java.util.Map;
 
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import org.springframework.security.core.Authentication;
import lombok.RequiredArgsConstructor;
import project.iot.Iot.dto.NotificationRequest; 
import project.iot.Iot.service.NotificationExampleService;
import project.iot.Iot.service.NotificationPollingService; 
@RestController
@RequestMapping("/api/device")
@RequiredArgsConstructor
public class NotificationController {
    private final NotificationExampleService notificationService;
    private final NotificationPollingService notificationPollingService;
    @PostMapping("/send")
    public String sendNotification(
            @RequestBody NotificationRequest notificationRequest) {
        return notificationService.messageAlert(
            notificationRequest.getTopic(), 
            notificationRequest.getTitle(), 
            notificationRequest.getAlert(),
            notificationRequest.getTimestamp());
    }
    @GetMapping("/unread")
    public ResponseEntity<?> getUnreadNotifications(Authentication authentication) {
        String userEmail = authentication.getName();
        List<Map<String,String>> notifications = notificationPollingService.getUnreadNotifications(userEmail);
        return ResponseEntity.ok(notifications);
    }
    @PostMapping("/mark-read/{notificationId}")
    public ResponseEntity<?> markAsRead(@PathVariable String notificationId) {
        notificationPollingService.markAsRead(notificationId);
        return ResponseEntity.ok(Map.of("message", "Marked as read"));
    }
}
