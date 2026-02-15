package project.iot.Iot.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;
import project.iot.Iot.dto.GraphResponse;
import project.iot.Iot.dto.ValueRequest;
import project.iot.Iot.service.HumidityService;

@RestController
@RequestMapping("/api/humidity")
@RequiredArgsConstructor
public class HumidityController {

    private final HumidityService humidityService;



    @GetMapping("/{roomId}/graph")
    public ResponseEntity<GraphResponse> getHumidityGraph(
        @PathVariable String roomId, 
        @RequestParam int minutes) {
        return ResponseEntity.ok(humidityService.getHumidityLast24Hours(roomId, minutes));
    }

    @GetMapping("/{roomId}")
    public ResponseEntity<ValueRequest> getHumidite(
            @PathVariable String roomId) {
        return ResponseEntity.ok(humidityService.getHumidite(roomId));
    }

}
