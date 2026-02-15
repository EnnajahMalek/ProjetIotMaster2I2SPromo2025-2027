package project.iot.Iot.Helper;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import project.iot.Iot.model.Agent;

public class StateHelper {
    private final MongoTemplate sensorMongoTemplate;

    public StateHelper(MongoTemplate sensorMongoTemplate) {
        this.sensorMongoTemplate = sensorMongoTemplate;
    }

    public void casClima(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("clima", true);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }

    public void casFire(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("clima", true);
        update.set("window", true);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }

    public void casLight(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("light", true);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }

    public void casGaz(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("window", true);
        update.set("clima", true);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }


    public void casClimaInverse(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("clima", false);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }

    public void casFireInverse(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("clima", false);
        update.set("window", false);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }

    public void casLightInverse(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("light", false);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }

    public void casGazInverse(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("window", false);
        update.set("clima", false);
        sensorMongoTemplate.updateFirst(query, update, Agent.class);
    }
}