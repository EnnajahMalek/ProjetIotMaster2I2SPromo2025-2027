package project.iot.Iot.dto;
 

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import project.iot.Iot.model.Alert; 

@Data
@NoArgsConstructor
@AllArgsConstructor
public class NotificationRequest {
    private String topic;
    private String title;  
    private Alert alert;
    private String timestamp;
}
