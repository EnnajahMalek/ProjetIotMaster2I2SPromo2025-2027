package project.iot.Iot.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Document(collection = "Room-Agents")
public class Agent {
    @Id
    private String _id;   
    
    @Field("id")
    private String id;
    @Field("light")
    private Boolean light;
    @Field("temperaturepref")
    private Integer tempPref;
    @Field("port")
    private Boolean portCapteur;
    @Field("window")
    private Boolean window;
    @Field("clima")
    private Boolean climatiseur;
}
//had le fichier shno fih, fih gha les variables des chambres, 
// je vuex dire que, light par exemple est une representation logique d'une ompoule 
// light=true-> on a lumiere et vice-versa
//le string id est utilise comme un cle qui lie les 2 documents