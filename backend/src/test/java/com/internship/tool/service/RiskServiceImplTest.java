package com.internship.tool.service;

import com.internship.tool.dto.RiskDto;
import com.internship.tool.entity.Risk;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.exception.ValidationException;
import com.internship.tool.repository.RiskRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;

import java.util.Collections;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class RiskServiceImplTest {

    @Mock
    private RiskRepository riskRepository;

    @Mock
    private EmailService emailService;

    @InjectMocks
    private RiskServiceImpl riskService;

    private Risk risk;
    private RiskDto riskDto;
    private UUID riskId;

    @BeforeEach
    void setUp() {
        riskId = UUID.randomUUID();
        risk = Risk.builder()
                .id(riskId)
                .title("Test Risk")
                .description("Test Description")
                .likelihood(3)
                .impact(4)
                .status("OPEN")
                .assigneeEmail("test@example.com")
                .build();

        riskDto = RiskDto.builder()
                .title("Test Risk")
                .description("Test Description")
                .likelihood(3)
                .impact(4)
                .status("OPEN")
                .assigneeEmail("test@example.com")
                .build();
    }

    // 1. Test get all risks successfully
    @Test
    void getAllRisks_Success() {
        Page<Risk> riskPage = new PageImpl<>(Collections.singletonList(risk));
        when(riskRepository.findAll(any(PageRequest.class))).thenReturn(riskPage);

        Page<RiskDto> result = riskService.getAllRisks(PageRequest.of(0, 10));

        assertNotNull(result);
        assertEquals(1, result.getTotalElements());
        assertEquals(risk.getTitle(), result.getContent().get(0).getTitle());
    }

    // 2. Test get risk by ID successfully
    @Test
    void getRiskById_Success() {
        when(riskRepository.findById(riskId)).thenReturn(Optional.of(risk));

        RiskDto result = riskService.getRiskById(riskId);

        assertNotNull(result);
        assertEquals(riskId, result.getId());
        assertEquals(risk.getTitle(), result.getTitle());
    }

    // 3. Test get risk by ID throws ResourceNotFoundException
    @Test
    void getRiskById_NotFound_ThrowsException() {
        when(riskRepository.findById(riskId)).thenReturn(Optional.empty());

        assertThrows(ResourceNotFoundException.class, () -> riskService.getRiskById(riskId));
    }

    // 4. Test create risk successfully
    @Test
    void createRisk_Success() {
        when(riskRepository.save(any(Risk.class))).thenReturn(risk);

        RiskDto result = riskService.createRisk(riskDto);

        assertNotNull(result);
        assertEquals(risk.getTitle(), result.getTitle());
        verify(riskRepository, times(1)).save(any(Risk.class));
        verify(emailService, times(1)).sendRiskCreatedEmail(risk.getAssigneeEmail(), risk.getTitle(), risk.getId());
    }

    // 5. Test create risk missing likelihood throws ValidationException
    @Test
    void createRisk_MissingLikelihood_ThrowsException() {
        riskDto.setLikelihood(null);

        assertThrows(ValidationException.class, () -> riskService.createRisk(riskDto));
        verify(riskRepository, never()).save(any(Risk.class));
    }

    // 6. Test create risk missing impact throws ValidationException
    @Test
    void createRisk_MissingImpact_ThrowsException() {
        riskDto.setImpact(null);

        assertThrows(ValidationException.class, () -> riskService.createRisk(riskDto));
        verify(riskRepository, never()).save(any(Risk.class));
    }

    // 7. Test create risk without email doesn't call EmailService
    @Test
    void createRisk_NoEmail_SuccessNoEmailSent() {
        riskDto.setAssigneeEmail(null);
        risk.setAssigneeEmail(null);
        when(riskRepository.save(any(Risk.class))).thenReturn(risk);

        RiskDto result = riskService.createRisk(riskDto);

        assertNotNull(result);
        verify(emailService, never()).sendRiskCreatedEmail(anyString(), anyString(), any(UUID.class));
    }

    // 8. Test create risk with empty email doesn't call EmailService
    @Test
    void createRisk_EmptyEmail_SuccessNoEmailSent() {
        riskDto.setAssigneeEmail("");
        risk.setAssigneeEmail("");
        when(riskRepository.save(any(Risk.class))).thenReturn(risk);

        RiskDto result = riskService.createRisk(riskDto);

        assertNotNull(result);
        verify(emailService, never()).sendRiskCreatedEmail(anyString(), anyString(), any(UUID.class));
    }

    // 9. Test get all risks returns empty page
    @Test
    void getAllRisks_Empty_ReturnsEmptyPage() {
        Page<Risk> emptyPage = new PageImpl<>(Collections.emptyList());
        when(riskRepository.findAll(any(PageRequest.class))).thenReturn(emptyPage);

        Page<RiskDto> result = riskService.getAllRisks(PageRequest.of(0, 10));

        assertNotNull(result);
        assertEquals(0, result.getTotalElements());
    }

    // 10. Test DTO mapping preserves all fields
    @Test
    void getRiskById_VerifiesDtoMapping() {
        when(riskRepository.findById(riskId)).thenReturn(Optional.of(risk));

        RiskDto result = riskService.getRiskById(riskId);

        assertEquals(risk.getId(), result.getId());
        assertEquals(risk.getTitle(), result.getTitle());
        assertEquals(risk.getDescription(), result.getDescription());
        assertEquals(risk.getLikelihood(), result.getLikelihood());
        assertEquals(risk.getImpact(), result.getImpact());
        assertEquals(risk.getStatus(), result.getStatus());
        assertEquals(risk.getAssigneeEmail(), result.getAssigneeEmail());
    }
}
