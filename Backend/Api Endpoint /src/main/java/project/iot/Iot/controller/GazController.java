package project.iot.Iot.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable; 
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import lombok.RequiredArgsConstructor;
import project.iot.Iot.dto.GraphResponse;
import project.iot.Iot.dto.ValueRequest;
import project.iot.Iot.service.GazService;


@RestController
@RequestMapping("/api/gaz")
@RequiredArgsConstructor
public class GazController {
    
    private final GazService gasService;

    @GetMapping("/{roomId}")
    public ResponseEntity<ValueRequest> getGasLevel(@PathVariable String roomId) {
        return ResponseEntity.ok(gasService.getGazLevel(roomId));
    }
    @GetMapping("/{roomId}/graph")
    public ResponseEntity<GraphResponse> getGasGraph(@PathVariable String roomId,
        @RequestParam long minutes) {
        return ResponseEntity.ok(gasService.getGasLast24Hours(roomId,minutes));
    }


}
