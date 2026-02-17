package project.iot.Iot.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import lombok.RequiredArgsConstructor;
import project.iot.Iot.service.ClimatiseurService; 
import project.iot.Iot.service.LightService; 
import project.iot.Iot.service.PortService; 
import project.iot.Iot.service.WindowService; 

@RestController
@RequestMapping("/api/room")
@RequiredArgsConstructor
public class RoomController {
    private final PortService portService; 
    private final ClimatiseurService climateService;
    private final LightService lightService;     
    private final WindowService windowService;
    @GetMapping("/light/{roomId}")
    public ResponseEntity<Boolean> getLightStatus(@PathVariable String roomId) {
        return ResponseEntity.ok(lightService.getLightStatus(roomId));
    }
    
    @PostMapping("/light/toggle/{roomId}")
    public ResponseEntity<Boolean> toggleLight(@PathVariable String roomId) {
        return ResponseEntity.ok(lightService.toggleLight(roomId));
    }
    
    @GetMapping("/climat/{roomId}")
    public ResponseEntity<Boolean> getACStatus(@PathVariable String roomId) {
        return ResponseEntity.ok(climateService.getStatusClimat(roomId));
    }
    
    @PostMapping("/climat/toggle/{roomId}")
    public ResponseEntity<Boolean> toggleAC(@PathVariable String roomId) {
        return ResponseEntity.ok(climateService.toggleClimatiseur(roomId));
    }
    
    @GetMapping("/door/{roomId}")
    public ResponseEntity<Boolean> isDoorOpen(@PathVariable String roomId) {
        return ResponseEntity.ok(portService.getPortStatus(roomId));
    }

    @GetMapping("/window/{roomId}")
    public ResponseEntity<Boolean> isWindowOpen(@PathVariable String roomId)
    {
        return ResponseEntity.ok(windowService.getStatusWindow(roomId));
    }
    @PostMapping("/window/toggle/{roomId}")
    public ResponseEntity<Boolean> toggleWindow(@PathVariable String roomId) {
        return ResponseEntity.ok(windowService.toggleWindow(roomId));
    }    
    













    // @PostMapping("/clima-notification/{roomId}")
    // public ResponseEntity<Void> climaNotif(
    //         @PathVariable String roomId) {
    //     notificiationService.ClimaNotification(roomId);
    //     return ResponseEntity.ok(null);
    // }  
    // @PostMapping("/light-notification/{roomId}")
    // public ResponseEntity<Void> fuiteGaz(
    //         @PathVariable String roomId) {
    //             notificiationService.ClimaNotification(roomId);
    //             return null;
    // }
    // @PostMapping("/gaz-error/{roomId}")
    // public ResponseEntity<Boolean> fuiteGaz(
    //         @PathVariable String roomId, 
    //         @RequestBody int temperature) {
    //     return ResponseEntity.ok(temperatureService.setPreferedTemp(roomId, temperature));
    // }









    
    
    
}