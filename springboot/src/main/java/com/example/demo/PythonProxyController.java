package com.example.demo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

@RestController
public class PythonProxyController {

    private final RestTemplate restTemplate = new RestTemplate();

    @Value("${python.service.url:http://pythonapp:8080}")
    private String pythonServiceUrl;

    @GetMapping("/api/python")
    public ResponseEntity<String> callPythonApp() {
        try {
            String pythonResponse = restTemplate.getForObject(pythonServiceUrl, String.class);
            return ResponseEntity.ok("Python says: " + pythonResponse);
        } catch (Exception ex) {
            return ResponseEntity.status(502)
                    .body("Unable to reach pythonapp at " + pythonServiceUrl + ": " + ex.getMessage());
        }
    }
}
