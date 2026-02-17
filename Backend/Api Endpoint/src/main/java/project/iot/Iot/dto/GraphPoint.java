package project.iot.Iot.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class GraphPoint {
    private String timestamp;  // ISO format: "2024-02-09T14:30:00"
    private long Value;
}