package project.iot.Iot.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;
import project.iot.Iot.dto.GraphResponse;
import project.iot.Iot.dto.TemperatureRequest;
import project.iot.Iot.dto.ValueRequest;
import project.iot.Iot.service.TemperatureService;
@RestController
@RequestMapping("/api/temperature")
@RequiredArgsConstructor
public class TemperatureController {
    
    private final TemperatureService temperatureService;


    @GetMapping("/{roomId}")
    public ResponseEntity<ValueRequest> getTemperature(@PathVariable String roomId) {
        return ResponseEntity.ok(temperatureService.getTemp(roomId));
    }
    
    @GetMapping("/{roomId}/graph")
    public ResponseEntity<GraphResponse> getTempGraph(
            @PathVariable String roomId,
            @RequestParam(defaultValue = "1440") long minutes 
            
            ) {
        return ResponseEntity.ok(temperatureService.getTemperatureLast24Hours(roomId, minutes));
    }
    @PostMapping("/set-preference/{roomId}")
    public ResponseEntity<Boolean> setPreference(
            @PathVariable String roomId, 
            @RequestBody TemperatureRequest request) {
        return ResponseEntity.ok(temperatureService.setPreferedTemp(roomId, request.getTemperature()));
    }
    @GetMapping("/get-preference/{roomId}")
    public ResponseEntity<Integer> setPreference(
            @PathVariable String roomId) {
        return ResponseEntity.ok(temperatureService.getTempPref(roomId));
    }









        // @GetMapping("/temperature/{roomId}/debug")
    // public ResponseEntity<String> debugQuery(@PathVariable String roomId) {
    //     temperatureService.debugQuery(roomId);
    //     return ResponseEntity.ok("Check console logs");
    // }
    // @GetMapping("/temperature/debug-agent/{roomId}")
    // public ResponseEntity<String> debugAgent(@PathVariable String roomId) {
    //     temperatureService.debugAgentUpdate(roomId, 25);
    //     return ResponseEntity.ok("Check console");
    // }
    

}
