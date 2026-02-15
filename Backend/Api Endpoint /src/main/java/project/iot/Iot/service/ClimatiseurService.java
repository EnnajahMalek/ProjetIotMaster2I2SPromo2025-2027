package project.iot.Iot.service;
 

import org.springframework.beans.factory.annotation.Qualifier; 
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service; 
import project.iot.Iot.model.Agent; 

@Service
public class ClimatiseurService {
    private final MongoTemplate sensorMongoTemplate;
    
    public ClimatiseurService(@Qualifier("sensorMongoTemplate") MongoTemplate sensorMongoTemplate) {
        this.sensorMongoTemplate = sensorMongoTemplate;
    }
    public Boolean getStatusClimat(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));    
        Agent agent = sensorMongoTemplate.findOne(query, Agent.class);
        
        if (agent != null) {
            return agent.getClimatiseur();
        }
        
        return null;
    }
    public Boolean toggleClimatiseur(String roomId)
    {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Agent agent = sensorMongoTemplate.findOne(query, Agent.class);
        
        Update update = new Update();
        update.set("clima", !agent.getClimatiseur());
       
        var result = sensorMongoTemplate.updateFirst(query, update, Agent.class);
        
        return result.getModifiedCount() > 0;
    
    }
}
