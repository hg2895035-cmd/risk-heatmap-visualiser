package com.internship.tool.controller;

import com.internship.tool.config.JwtUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
@Tag(name = "Authentication", description = "Dummy API for getting JWT token")
public class AuthController {

    private final JwtUtil jwtUtil;

    @Operation(summary = "Generate a JWT token for testing")
    @PostMapping("/login")
    public ResponseEntity<Map<String, String>> login(@RequestParam String username) {
        String token = jwtUtil.generateToken(username, "ROLE_ADMIN", 1L);
        return ResponseEntity.ok(Map.of("token", token));
    }
}
