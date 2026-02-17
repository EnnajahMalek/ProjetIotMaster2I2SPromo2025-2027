package project.iot.Iot.model;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import java.time.LocalDateTime;

@Data
@Document(collection = "notifications")
public class Notification {
    @Id
    private String id;
    private String userEmail;
    private String title;
    private String body;
    private String roomId;
    private String alertType;
    private boolean read;
    private LocalDateTime createdAt;
    
    public Notification() {
        this.read = false;
        this.createdAt = LocalDateTime.now();
    }
}