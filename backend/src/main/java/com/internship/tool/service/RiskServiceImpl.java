package com.internship.tool.service;

import com.internship.tool.dto.RiskDto;
import com.internship.tool.entity.Risk;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.exception.ValidationException;
import com.internship.tool.repository.RiskRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;

import java.util.UUID;

@Service
@RequiredArgsConstructor
public class RiskServiceImpl implements RiskService {

    private final RiskRepository riskRepository;
    private final EmailService emailService;

    @Override
    @Cacheable(value = "risks", key = "#pageable.pageNumber + '-' + #pageable.pageSize")
    public Page<RiskDto> getAllRisks(Pageable pageable) {
        return riskRepository.findAll(pageable).map(this::mapToDto);
    }

    @Override
    @Cacheable(value = "risk", key = "#id")
    public RiskDto getRiskById(UUID id) {
        Risk risk = riskRepository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Risk not found with id: " + id));
        return mapToDto(risk);
    }

    @Override
    @CacheEvict(value = {"risks", "risk"}, allEntries = true)
    public RiskDto createRisk(RiskDto riskDto) {
        if (riskDto.getLikelihood() == null || riskDto.getImpact() == null) {
            throw new ValidationException("Likelihood and Impact are required.");
        }

        Risk risk = mapToEntity(riskDto);
        Risk savedRisk = riskRepository.save(risk);
        
        if (savedRisk.getAssigneeEmail() != null && !savedRisk.getAssigneeEmail().isEmpty()) {
            emailService.sendRiskCreatedEmail(savedRisk.getAssigneeEmail(), savedRisk.getTitle(), savedRisk.getId());
        }

        return mapToDto(savedRisk);
    }

    private RiskDto mapToDto(Risk risk) {
        return RiskDto.builder()
                .id(risk.getId())
                .title(risk.getTitle())
                .description(risk.getDescription())
                .likelihood(risk.getLikelihood())
                .impact(risk.getImpact())
                .status(risk.getStatus())
                .assigneeEmail(risk.getAssigneeEmail())
                .createdAt(risk.getCreatedAt())
                .updatedAt(risk.getUpdatedAt())
                .build();
    }

    private Risk mapToEntity(RiskDto riskDto) {
        return Risk.builder()
                .title(riskDto.getTitle())
                .description(riskDto.getDescription())
                .likelihood(riskDto.getLikelihood())
                .impact(riskDto.getImpact())
                .status(riskDto.getStatus())
                .assigneeEmail(riskDto.getAssigneeEmail())
                .build();
    }
}
