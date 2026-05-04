package com.internship.tool.controller;

import com.internship.tool.dto.RiskItemRequest;
import com.internship.tool.dto.RiskItemResponse;
import com.internship.tool.dto.StatsResponse;
import com.internship.tool.service.RiskItemService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/risks")
@RequiredArgsConstructor
@Tag(name = "Risk Items", description = "Risk item management endpoints")
@SecurityRequirement(name = "Bearer Authentication")
public class RiskItemController {

    private final RiskItemService riskItemService;

    @GetMapping
    @Operation(summary = "List all risks", description = "Get paginated list of all risk items")
    public ResponseEntity<Page<RiskItemResponse>> getAllRisks(
            @Parameter(description = "Page number (0-indexed)") @RequestParam(defaultValue = "0") int page,
            @Parameter(description = "Page size") @RequestParam(defaultValue = "10") int size,
            @Parameter(description = "Sort field") @RequestParam(defaultValue = "createdAt") String sortBy,
            @Parameter(description = "Sort direction") @RequestParam(defaultValue = "desc") String sortDir) {
        return ResponseEntity.ok(riskItemService.getAllRisks(page, size, sortBy, sortDir));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get risk by ID", description = "Get a single risk item by its ID")
    public ResponseEntity<RiskItemResponse> getRiskById(
            @Parameter(description = "Risk ID") @PathVariable Long id) {
        return ResponseEntity.ok(riskItemService.getRiskById(id));
    }

    @PostMapping
    @PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
    @Operation(summary = "Create risk", description = "Create a new risk item")
    public ResponseEntity<RiskItemResponse> createRisk(
            @Valid @RequestBody RiskItemRequest request) {
        RiskItemResponse response = riskItemService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
    @Operation(summary = "Update risk", description = "Update an existing risk item")
    public ResponseEntity<RiskItemResponse> updateRisk(
            @Parameter(description = "Risk ID") @PathVariable Long id,
            @Valid @RequestBody RiskItemRequest request) {
        return ResponseEntity.ok(riskItemService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")
    @Operation(summary = "Delete risk", description = "Soft delete a risk item")
    public ResponseEntity<Map<String, String>> deleteRisk(
            @Parameter(description = "Risk ID") @PathVariable Long id) {
        riskItemService.delete(id);
        return ResponseEntity.ok(Map.of("message", "Risk deleted successfully"));
    }

    @GetMapping("/search")
    @Operation(summary = "Search risks", description = "Search risks by title, description, or owner")
    public ResponseEntity<Page<RiskItemResponse>> searchRisks(
            @Parameter(description = "Search query") @RequestParam String q,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size) {
        return ResponseEntity.ok(riskItemService.search(q, page, size));
    }

    @GetMapping("/stats")
    @Operation(summary = "Get statistics", description = "Get dashboard statistics for risk items")
    public ResponseEntity<StatsResponse> getStats() {
        return ResponseEntity.ok(riskItemService.getStats());
    }

    @PostMapping("/{id}/upload")
    @PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
    @Operation(summary = "Upload file", description = "Upload an attachment for a risk item")
    public ResponseEntity<Map<String, String>> uploadFile(
            @PathVariable Long id,
            @RequestParam("file") MultipartFile file) {
        String filename = riskItemService.uploadFile(id, file);
        return ResponseEntity.ok(Map.of("filename", filename));
    }

    @GetMapping("/export")
    @Operation(summary = "Export risks", description = "Export all risks as CSV")
    public ResponseEntity<List<RiskItemResponse>> exportRisks() {
        Page<RiskItemResponse> page = riskItemService.getAllRisks(0, 10000, "createdAt", "desc");
        return ResponseEntity.ok(page.getContent());
    }
}
