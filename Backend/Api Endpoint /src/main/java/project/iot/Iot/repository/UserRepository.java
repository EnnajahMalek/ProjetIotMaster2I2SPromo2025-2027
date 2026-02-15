package project.iot.Iot.repository;

import org.springframework.data.mongodb.repository.MongoRepository;
import project.iot.Iot.model.User;
import java.util.Optional;

public interface UserRepository extends MongoRepository<User, String> {
    Optional<User> findByEmail(String email);
    Boolean existsByEmail(String email);
}