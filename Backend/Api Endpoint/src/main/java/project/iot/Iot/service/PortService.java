package project.iot.Iot.service;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import project.iot.Iot.model.Agent;

@Service
public class PortService {
    private final MongoTemplate sensorMongoTemplate;
    
    public PortService(@Qualifier("sensorMongoTemplate") MongoTemplate sensorMongoTemplate) {
        this.sensorMongoTemplate = sensorMongoTemplate;
    }
    
    public Boolean getPortStatus(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        
        Agent agent = sensorMongoTemplate.findOne(query, Agent.class);
        
        if (agent != null) {
            return agent.getPortCapteur();
        }
        
        return null;
    }
    
}
