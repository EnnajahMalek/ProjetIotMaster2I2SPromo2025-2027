// package project.iot.Iot.security;

// import org.springframework.beans.factory.annotation.Value;
// import org.springframework.stereotype.Component;
// import org.springframework.web.filter.OncePerRequestFilter;

// import javax.crypto.Mac;
// import javax.crypto.spec.SecretKeySpec;
// import jakarta.servlet.FilterChain;
// import jakarta.servlet.ServletException;
// import jakarta.servlet.http.HttpServletRequest;
// import jakarta.servlet.http.HttpServletResponse;
// import java.io.IOException;
// import java.nio.charset.StandardCharsets;
// import java.security.MessageDigest;
// import java.time.Instant;
// import java.util.Arrays;
// import java.util.List;

// @Component
// public class DeviceAuthFilter extends OncePerRequestFilter {

//     @Value("${device.user.id}")
//     private String deviceToken;

//     @Value("${device.secret}")
//     private String deviceSecret;

//     @Value("${allowed.device.id}")
//     private String allowedDeviceId;

//     // Paths that require device authentication (only Flask endpoints)
//     private static final List<String> DEVICE_AUTH_PATHS = Arrays.asList(
//         "/api/device/",     
//         "/api/flask/" 
//         "/api/data"      
//     );

//     @Override
//     protected boolean shouldNotFilter(HttpServletRequest request) {
//         String path = request.getRequestURI();
        
//         return DEVICE_AUTH_PATHS.stream()
//             .noneMatch(path::startsWith);
//     }

//     @Override
//     protected void doFilterInternal(HttpServletRequest request, 
//                                    HttpServletResponse response, 
//                                    FilterChain filterChain) 
//             throws ServletException, IOException {

//         String deviceId = request.getHeader("X-Device-ID");
//         String deviceToken = request.getHeader("X-Device-Token");
//         String timestamp = request.getHeader("X-Timestamp");
//         String signature = request.getHeader("X-Signature");

//         if (!verifyRequest(deviceId, deviceToken, timestamp, signature, request)) {
//             response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
//             response.getWriter().write("{\"error\":\"Unauthorized device\"}");
//             return;
//         }

//         filterChain.doFilter(request, response);
//     }

//     private boolean verifyRequest(String deviceId, String token, String timestamp, 
//                                  String signature, HttpServletRequest request) {
//         try {
//             if (!allowedDeviceId.equals(deviceId)) {
//                 return false;
//             }

//             if (!this.deviceToken.equals(token)) {
//                 return false;
//             }

//             long requestTime = Long.parseLong(timestamp);
//             long currentTime = Instant.now().getEpochSecond();
//             if (Math.abs(currentTime - requestTime) > 300) {
//                 return false;
//             }

//             String body = request.getReader().lines()
//                 .reduce("", (accumulator, actual) -> accumulator + actual);

//             String message = deviceId + ":" + timestamp + ":" + body;
//             String expectedSignature = generateSignature(message);

//             return MessageDigest.isEqual(
//                 signature.getBytes(StandardCharsets.UTF_8),
//                 expectedSignature.getBytes(StandardCharsets.UTF_8)
//             );

//         } catch (Exception e) {
//             return false;
//         }
//     }

//     private String generateSignature(String message) throws Exception {
//         Mac mac = Mac.getInstance("HmacSHA256");
//         SecretKeySpec secretKey = new SecretKeySpec(
//             deviceSecret.getBytes(StandardCharsets.UTF_8), 
//             "HmacSHA256"
//         );
//         mac.init(secretKey);

//         byte[] hash = mac.doFinal(message.getBytes(StandardCharsets.UTF_8));
//         return bytesToHex(hash);
//     }

//     private String bytesToHex(byte[] bytes) {
//         StringBuilder result = new StringBuilder();
//         for (byte b : bytes) {
//             result.append(String.format("%02x", b));
//         }
//         return result.toString();
//     }
// }