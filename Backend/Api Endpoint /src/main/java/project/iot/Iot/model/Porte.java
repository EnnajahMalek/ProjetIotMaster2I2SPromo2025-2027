package project.iot.Iot.model;

import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


@Data
@NoArgsConstructor
@AllArgsConstructor
public class Porte {
    @Field("sensor_id")
    private String sensor_id;
    @Field("sensor_type")
    private String sensor_type;
    @Field("value")
    private Boolean value;
    @Field("timestamp")
    private String timestamp;
}
