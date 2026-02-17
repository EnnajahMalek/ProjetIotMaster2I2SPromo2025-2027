package project.iot.Iot.service;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;
import org.springframework.stereotype.Service;

import project.iot.Iot.dto.GraphPoint;
import project.iot.Iot.dto.GraphResponse;
import project.iot.Iot.dto.ValueRequest;
import project.iot.Iot.model.Agent;
import project.iot.Iot.model.Room;
 
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class TemperatureService {
    
    private final MongoTemplate sensorMongoTemplate;
    private static final int TARGET_POINTS = 12;
     
    public TemperatureService(@Qualifier("sensorMongoTemplate") MongoTemplate sensorMongoTemplate) {
        this.sensorMongoTemplate = sensorMongoTemplate;
    }
    
    public ValueRequest getTemp(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        query.with(Sort.by(Sort.Direction.DESC, "timestamp"));
        query.limit(1);
        
        Room room = sensorMongoTemplate.findOne(query, Room.class);
        
        if (room != null) {
            return new ValueRequest("Temperature", String.valueOf(room.getTempCapteur()));
        }
        return new ValueRequest("Temperature", "N/A");
    }
    
    public Boolean setPreferedTemp(String roomId, int value) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Update update = new Update();
        update.set("temperaturepref", value); 
        
        var result = sensorMongoTemplate.updateFirst(query, update, Agent.class);
        return result.getModifiedCount() > 0;
    }
    public Integer getTempPref(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        Agent agent = sensorMongoTemplate.findOne(query, Agent.class);
        
        if(agent!=null)
        {
            return agent.getTempPref();
        }
        return null;
    }
    
    
 
    public GraphResponse getTemperatureLast24Hours(String roomId, long minutes) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime from = now.minusMinutes(minutes);
        
        Query query = new Query();
        query.addCriteria(
            Criteria.where("id").is(roomId)
                .and("timestamp").gte(from.toString())
        );
        query.with(Sort.by(Sort.Direction.ASC, "timestamp"));
        
        List<Room> rooms = sensorMongoTemplate.find(query, Room.class);
        
        long bucketSizeMinutes = 120; // 2 hours
        int numBuckets = (int) (minutes / bucketSizeMinutes);
        if (numBuckets < 1) numBuckets = 1;
        
        // Create all hourly buckets (even if empty)
        Map<String, List<Double>> allBuckets = new LinkedHashMap<>();
        for (int i = 0; i < numBuckets; i++) {
            LocalDateTime bucketTime = from.plusMinutes(i * bucketSizeMinutes);
            allBuckets.put(bucketTime.toString(), new ArrayList<>());
        }
        
        // Fill buckets with actual data
        if (!rooms.isEmpty()) {
            for (Room room : rooms) {
                String timestampStr = parseTimestamp(room.getTimestamp());
                LocalDateTime dt = LocalDateTime.parse(timestampStr);
                long minutesSinceStart = java.time.Duration.between(from, dt).toMinutes();
                long bucketIndex = Math.min(numBuckets - 1, minutesSinceStart / bucketSizeMinutes);
                
                LocalDateTime bucketTime = from.plusMinutes(bucketIndex * bucketSizeMinutes);
                String bucketKey = bucketTime.toString();
                
                if (allBuckets.containsKey(bucketKey)) {
                    allBuckets.get(bucketKey).add(room.getTempCapteur());
                }
            }
        }
        
        // Convert to data points with forward-fill for missing values
        List<GraphPoint> dataPoints = new ArrayList<>();
        Integer lastValue = null;
        
        // Add DateTimeFormatter for hour formatting
        DateTimeFormatter hourFormatter = DateTimeFormatter.ofPattern("HH");
        
        for (Map.Entry<String, List<Double>> entry : allBuckets.entrySet()) {
            int value;
            if (!entry.getValue().isEmpty()) {
                // Calculate average if data exists
                value = (int) Math.round(
                    entry.getValue().stream()
                        .mapToDouble(Double::doubleValue)
                        .average()
                        .orElse(0)
                );
                lastValue = value;
            } else if (lastValue != null) {
                // Forward-fill: use last known value
                value = lastValue;
            } else {
                // No data yet, use 0 or a default value
                value = 0;
            }
            
            // Format timestamp to show only hour (HH:mm format)
            LocalDateTime bucketTime = LocalDateTime.parse(entry.getKey());
            String formattedTime = bucketTime.format(hourFormatter);
            
            dataPoints.add(new GraphPoint(formattedTime, value));
        }
        
        GraphResponse response = new GraphResponse();
        response.setRoomId(roomId);
        response.setPoints(dataPoints);
        return response;
    }
    private String parseTimestamp(String timestampStr) {
        if (timestampStr.contains("+")) {
            timestampStr = timestampStr.substring(0, timestampStr.indexOf('+'));
        } else if (timestampStr.contains("Z")) {
            timestampStr = timestampStr.substring(0, timestampStr.indexOf('Z'));
        }
        if (timestampStr.length() > 23) {
            timestampStr = timestampStr.substring(0, 23);
        }
        return timestampStr;
    }
    
    public void debugQuery(String roomId) {
        // Test 1: Find by ID only
        Query query1 = new Query();
        query1.addCriteria(Criteria.where("id").is(roomId));
        List<Room> rooms1 = sensorMongoTemplate.find(query1, Room.class);
        System.out.println("=== Test 1: Query by ID only ===");
        System.out.println("Found " + rooms1.size() + " rooms");
        if (!rooms1.isEmpty()) {
            rooms1.forEach(r -> {
                System.out.println("Room ID: " + r.getId());
                System.out.println("Timestamp: " + r.getTimestamp());
                System.out.println("Timestamp class: " + (r.getTimestamp() != null ? r.getTimestamp().getClass() : "null"));
                System.out.println("Temp: " + r.getTempCapteur());
                System.out.println("---");
            });
        }
        
        // Test 2: Find all documents in collection
        List<Room> allRooms = sensorMongoTemplate.findAll(Room.class);
        System.out.println("=== Test 2: All documents ===");
        System.out.println("Total documents: " + allRooms.size());
        allRooms.forEach(r -> System.out.println("ID: " + r.getId() + ", Timestamp: " + r.getTimestamp()));
        
        // Test 3: Raw query
        System.out.println("=== Test 3: Collection name ===");
        System.out.println("Collection: " + sensorMongoTemplate.getCollectionName(Room.class));
    }

    public void debugAgentUpdate(String roomId, int value) {
        // Test 1: Find by id
        Query query1 = new Query();
        query1.addCriteria(Criteria.where("id").is(roomId));
        Agent agent = sensorMongoTemplate.findOne(query1, Agent.class);
        
        System.out.println("=== Looking for roomId: " + roomId + " ===");
        System.out.println("Found agent: " + agent);
        
        if (agent != null) {
            System.out.println("Agent ID: " + agent.getId());
            System.out.println("Agent _id: " + agent.get_id());
            System.out.println("Current tempPref: " + agent.getTempPref());
        }
        
        // Test 2: Show all agents
        List<Agent> all = sensorMongoTemplate.findAll(Agent.class);
        System.out.println("=== All agents in collection ===");
        all.forEach(a -> System.out.println("ID: " + a.getId() + ", _id: " + a.get_id()));
        
        // Test 3: Try the update
        if (agent != null) {
            Update update = new Update();
            update.set("temperaturepref", value);
            var result = sensorMongoTemplate.updateFirst(query1, update, Agent.class);
            System.out.println("Modified count: " + result.getModifiedCount());
            System.out.println("Matched count: " + result.getMatchedCount());
        }
    }
}