package project.iot.Iot.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

// import java.time.Instant;
// import java.time.LocalDateTime; 
@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "sensor_logs")
public class Room {
    
    @Id
    private String _id;   
    
    @Field("id")
    private String id;
    
    @Field("tempCapteur")
    private Double tempCapteur;
    
    @Field("humiditeCapteur")
    private Double humiditeCapteur;
    
    @Field("gazCapteur")
    private Double gazCapteur;
    
    @Field("motion")
    private Motion motion;
    
    @Field("porte")
    private Porte porte;
    @Field("timestamp")
    private String timestamp;  

    /*
    ---->temp >>>> oooo khasi nhbtha ----> climatiseur ON 
    ---->temp<<<<< ooooo khasi ntfiha ----> clima OFF

Capteurs->BD->BackendFlask(Traitement)-ooooo probleme->BackendJava ---Notificiation--> App mobile 
                                                          |
                                                          --Clima ON->Capteurs-->temperature diminue
                                                                
                                                        
    */
}
