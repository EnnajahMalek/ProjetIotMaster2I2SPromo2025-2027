package project.iot.Iot.service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import project.iot.Iot.dto.GraphPoint;
import project.iot.Iot.dto.GraphResponse;
import project.iot.Iot.dto.ValueRequest;
import project.iot.Iot.model.Room;

@Service
public class GazService {
    
    private final MongoTemplate sensorMongoTemplate; 
    
    public GazService(@Qualifier("sensorMongoTemplate") MongoTemplate sensorMongoTemplate) {
        this.sensorMongoTemplate = sensorMongoTemplate;
    }
    
    public ValueRequest getGazLevel(String roomId) {
        Query query = new Query();
        query.addCriteria(Criteria.where("id").is(roomId));
        query.with(Sort.by(Sort.Direction.DESC, "timestamp"));
        query.limit(1);
        
        Room room = sensorMongoTemplate.findOne(query, Room.class);
        
        if (room != null) {
            return new ValueRequest("Gaz", String.valueOf(room.getGazCapteur()));
        }
        return new ValueRequest("Gaz", "N/A");
    }
    
    public GraphResponse getGasLast24Hours(String roomId, long minutes) {
        LocalDateTime now = LocalDateTime.now();
        LocalDateTime from = now.minusMinutes(minutes);
        
        Query query = new Query();
        query.addCriteria(
            Criteria.where("id").is(roomId)
                .and("timestamp").gte(from.toString())
        );
        query.with(Sort.by(Sort.Direction.ASC, "timestamp"));
        
        List<Room> rooms = sensorMongoTemplate.find(query, Room.class);
         
        long bucketSizeMinutes = 120;  
        int numBuckets = (int) (minutes / bucketSizeMinutes);
        if (numBuckets < 1) numBuckets = 1;
         
        Map<String, List<Double>> allBuckets = new LinkedHashMap<>();
        for (int i = 0; i < numBuckets; i++) {
            LocalDateTime bucketTime = from.plusMinutes(i * bucketSizeMinutes);
            allBuckets.put(bucketTime.toString(), new ArrayList<>());
        }
         
        if (!rooms.isEmpty()) {
            for (Room room : rooms) {
                String timestampStr = parseTimestamp(room.getTimestamp());
                LocalDateTime dt = LocalDateTime.parse(timestampStr);
                long minutesSinceStart = java.time.Duration.between(from, dt).toMinutes();
                long bucketIndex = Math.min(numBuckets - 1, minutesSinceStart / bucketSizeMinutes);
                
                LocalDateTime bucketTime = from.plusMinutes(bucketIndex * bucketSizeMinutes);
                String bucketKey = bucketTime.toString();
                
                if (allBuckets.containsKey(bucketKey)) {
                    allBuckets.get(bucketKey).add(room.getGazCapteur());
                }
            }
        }
        
        List<GraphPoint> dataPoints = new ArrayList<>();
        Integer lastValue = null;
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
}