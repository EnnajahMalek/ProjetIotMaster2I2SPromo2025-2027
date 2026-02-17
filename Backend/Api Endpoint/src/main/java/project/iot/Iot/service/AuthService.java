package project.iot.Iot.service;

import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import project.iot.Iot.dto.AuthResponse;
import project.iot.Iot.dto.LoginRequest;
import project.iot.Iot.dto.RegisterRequest;
import project.iot.Iot.model.User;
import project.iot.Iot.repository.UserRepository;
import project.iot.Iot.security.JwtUtil;

@Service
@RequiredArgsConstructor
public class AuthService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    
    public AuthResponse register(RegisterRequest request) {
        // Check if email already exists
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new RuntimeException("Email already exists");
        }
        
        // Create new user
        User user = new User();
        user.setEmail(request.getEmail());
        user.setPassword(passwordEncoder.encode(request.getPassword()));
        user.setName(request.getName());
        user.setRole("USER");
        
        userRepository.save(user);
        
        // Generate token
        String token = jwtUtil.generateToken(user.getEmail());
        
        return new AuthResponse(token, user.getEmail(), user.getName());
    }
    
    public AuthResponse login(LoginRequest request) {
        // Find user
        User user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new RuntimeException("Invalid credentials"));
         
        if (!passwordEncoder.matches(request.getPassword(), user.getPassword())) {
            throw new RuntimeException("Invalid credentials");
        }
         
        String token = jwtUtil.generateToken(user.getEmail());
        
        return new AuthResponse(token, user.getEmail(), user.getName());
    }
}