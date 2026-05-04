package com.internship.tool.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class RiskDto {
    private UUID id;

    @NotBlank(message = "Title is required")
    private String title;

    private String description;

    @NotNull(message = "Likelihood is required")
    @Min(value = 1, message = "Likelihood must be at least 1")
    @Max(value = 5, message = "Likelihood must be at most 5")
    private Integer likelihood;

    @NotNull(message = "Impact is required")
    @Min(value = 1, message = "Impact must be at least 1")
    @Max(value = 5, message = "Impact must be at most 5")
    private Integer impact;

    @NotBlank(message = "Status is required")
    private String status;

    private String assigneeEmail;

    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
