package project.iot.Iot.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.SimpleMongoClientDatabaseFactory;

@Configuration
public class MongoConfig {
    
    @Value("${spring.data.mongodb.uri}")
    private String primaryMongoUri;
    
    @Value("${mongodb.sensors.uri}")
    private String sensorsMongoUri;
     
    @Primary
    @Bean(name = {"mongoTemplate", "primaryMongoTemplate"})
    public MongoTemplate primaryMongoTemplate() {
        return new MongoTemplate(new SimpleMongoClientDatabaseFactory(primaryMongoUri));
    }
     
    @Bean(name = "sensorMongoTemplate")
    public MongoTemplate sensorMongoTemplate() {
        return new MongoTemplate(new SimpleMongoClientDatabaseFactory(sensorsMongoUri));
    }
}