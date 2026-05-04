package com.internship.tool.service;

import com.internship.tool.dto.LoginRequest;
import com.internship.tool.dto.LoginResponse;
import com.internship.tool.dto.RegisterRequest;
import com.internship.tool.entity.AppUser;
import com.internship.tool.entity.UserRole;
import com.internship.tool.exception.ValidationException;
import com.internship.tool.config.JwtUtil;
import com.internship.tool.repository.AppUserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Slf4j
public class AuthService {

    private final AppUserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    private final AuthenticationManager authenticationManager;

    @Transactional
    public LoginResponse login(LoginRequest request) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(request.getEmail(), request.getPassword())
        );

        AppUser user = userRepository.findByEmail(request.getEmail())
                .orElseThrow(() -> new ValidationException("User not found"));

        String token = jwtUtil.generateToken(user.getEmail(), user.getRole().name(), user.getId());

        log.info("User logged in: {}", user.getEmail());
        return LoginResponse.builder()
                .token(token)
                .user(LoginResponse.UserDto.fromEntity(user))
                .build();
    }

    @Transactional
    public LoginResponse.UserDto register(RegisterRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new ValidationException("Email already registered");
        }

        AppUser user = AppUser.builder()
                .email(request.getEmail())
                .passwordHash(passwordEncoder.encode(request.getPassword()))
                .name(request.getName())
                .role(request.getRole() != null ? request.getRole() : UserRole.VIEWER)
                .build();

        AppUser savedUser = userRepository.save(user);
        log.info("New user registered: {}", savedUser.getEmail());

        return LoginResponse.UserDto.fromEntity(savedUser);
    }

    public String refreshToken(String currentToken) {
        String email = jwtUtil.extractEmail(currentToken);
        AppUser user = userRepository.findByEmail(email)
                .orElseThrow(() -> new ValidationException("User not found"));

        return jwtUtil.generateToken(user.getEmail(), user.getRole().name(), user.getId());
    }
}
