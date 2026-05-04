package com.internship.tool.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import org.springframework.boot.web.client.RestTemplateBuilder;

import java.time.Duration;
import java.util.Map;

@Component
public class AiServiceClient {

    private final RestTemplate restTemplate;

    @Value("${ai.service.url:http://localhost:5000}")
    private String aiServiceUrl;

    public AiServiceClient(RestTemplateBuilder builder) {
        this.restTemplate = builder
                .setConnectTimeout(Duration.ofSeconds(10))
                .setReadTimeout(Duration.ofSeconds(10))
                .build();
    }

    // Call /describe endpoint
    public String describe(String text) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, String> body = Map.of("text", text);
            HttpEntity<Map<String, String>> request = new HttpEntity<>(body, headers);
            ResponseEntity<String> response = restTemplate.postForEntity(
                    aiServiceUrl + "/describe", request, String.class);
            return response.getBody();
        } catch (Exception e) {
            System.err.println("AI Service /describe failed: " + e.getMessage());
            return null;
        }
    }

    // Call /recommend endpoint
    public String recommend(String text) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, String> body = Map.of("text", text);
            HttpEntity<Map<String, String>> request = new HttpEntity<>(body, headers);
            ResponseEntity<String> response = restTemplate.postForEntity(
                    aiServiceUrl + "/recommend", request, String.class);
            return response.getBody();
        } catch (Exception e) {
            System.err.println("AI Service /recommend failed: " + e.getMessage());
            return null;
        }
    }

    // Call /generate-report endpoint
    public String generateReport(String text) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, String> body = Map.of("text", text);
            HttpEntity<Map<String, String>> request = new HttpEntity<>(body, headers);
            ResponseEntity<String> response = restTemplate.postForEntity(
                    aiServiceUrl + "/generate-report", request, String.class);
            return response.getBody();
        } catch (Exception e) {
            System.err.println("AI Service /generate-report failed: " + e.getMessage());
            return null;
        }
    }

    // Call /health endpoint
    public String health() {
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(
                    aiServiceUrl + "/health", String.class);
            return response.getBody();
        } catch (Exception e) {
            System.err.println("AI Service /health failed: " + e.getMessage());
            return null;
        }
    }
}