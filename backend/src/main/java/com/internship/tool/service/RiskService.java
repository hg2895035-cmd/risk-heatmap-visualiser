package com.internship.tool.service;

import com.internship.tool.dto.RiskDto;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.UUID;

public interface RiskService {
    Page<RiskDto> getAllRisks(Pageable pageable);
    RiskDto getRiskById(UUID id);
    RiskDto createRisk(RiskDto riskDto);
}
