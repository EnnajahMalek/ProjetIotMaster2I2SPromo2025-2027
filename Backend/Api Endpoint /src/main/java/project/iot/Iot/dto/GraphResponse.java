package project.iot.Iot.dto;

import java.util.List;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class GraphResponse {
    

    private String roomId;  // identif room
    private List<GraphPoint> points;// tous les point du graph
}