package project.iot.Iot.dto;

import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class ValueRequest {
    private String key;
    private String value;
}
