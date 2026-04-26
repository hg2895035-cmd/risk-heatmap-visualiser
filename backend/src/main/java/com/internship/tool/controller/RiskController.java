package com.internship.tool.controller;

import com.internship.tool.dto.RiskDto;
import com.internship.tool.service.RiskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/risks")
@RequiredArgsConstructor
@Tag(name = "Risk Management", description = "APIs for managing risks")
public class RiskController {

    private final RiskService riskService;

    @Operation(summary = "Get all risks with pagination")
    @GetMapping("/all")
    public ResponseEntity<Page<RiskDto>> getAllRisks(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        Pageable pageable = PageRequest.of(page, size);
        return ResponseEntity.ok(riskService.getAllRisks(pageable));
    }

    @Operation(summary = "Get a risk by ID")
    @GetMapping("/{id}")
    public ResponseEntity<RiskDto> getRiskById(@PathVariable UUID id) {
        return ResponseEntity.ok(riskService.getRiskById(id));
    }

    @Operation(summary = "Create a new risk")
    @PostMapping("/create")
    public ResponseEntity<RiskDto> createRisk(@Valid @RequestBody RiskDto riskDto) {
        return new ResponseEntity<>(riskService.createRisk(riskDto), HttpStatus.CREATED);
    }
}
