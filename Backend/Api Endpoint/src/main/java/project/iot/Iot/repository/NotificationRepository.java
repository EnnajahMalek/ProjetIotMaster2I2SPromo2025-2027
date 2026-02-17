package project.iot.Iot.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import project.iot.Iot.model.Notification;
import java.util.List;

public interface NotificationRepository extends MongoRepository<Notification, String> {
    List<Notification> findByUserEmailAndReadFalse(String userEmail);
}