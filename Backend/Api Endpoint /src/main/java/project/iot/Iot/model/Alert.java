package project.iot.Iot.model;

import lombok.Data;

@Data
public class Alert {
    private Boolean is_anomaly;//true-->
    private String description;
    private String roomId;
    private AlertType type;
    private Severity severity;//medium wla high wla ciritcal
}
