package com.internship.tool.controller;

import com.internship.tool.dto.LoginRequest;
import com.internship.tool.dto.LoginResponse;
import com.internship.tool.dto.RegisterRequest;
import com.internship.tool.service.AuthService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
@Tag(name = "Authentication", description = "Authentication endpoints")
public class AuthController {

    private final AuthService authService;

    @PostMapping("/login")
    @Operation(summary = "Login", description = "Authenticate user and return JWT token")
    public ResponseEntity<LoginResponse> login(@Valid @RequestBody LoginRequest request) {
        LoginResponse response = authService.login(request);
        return ResponseEntity.ok(response);
    }

    @PostMapping("/register")
    @Operation(summary = "Register", description = "Register a new user with VIEWER role")
    public ResponseEntity<LoginResponse.UserDto> register(@Valid @RequestBody RegisterRequest request) {
        LoginResponse.UserDto response = authService.register(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/refresh")
    @Operation(summary = "Refresh token", description = "Refresh JWT token")
    public ResponseEntity<LoginResponse> refresh(@RequestHeader("Authorization") String authHeader) {
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            String newToken = authService.refreshToken(token);
            return ResponseEntity.ok(LoginResponse.builder().token(newToken).build());
        }
        return ResponseEntity.badRequest().build();
    }
}
