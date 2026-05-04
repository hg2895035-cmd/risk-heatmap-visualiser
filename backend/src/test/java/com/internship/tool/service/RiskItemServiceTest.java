package com.internship.tool.service;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.data.domain.Page;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertNotNull;

@ExtendWith(MockitoExtension.class)
class RiskItemServiceTest {

    @Mock
    private EmailService emailService;

    @Mock
    private ObjectMapper objectMapper;

    @InjectMocks
    private RiskItemService riskItemService;

    @Test
    void testGetAllRisks() {
        Page<Map<String, Object>> result = riskItemService.getAllRisks(0, 10, "id", "asc");
        assertNotNull(result);
    }

    @Test
    void testGetRiskById() {
        Map<String, Object> result = riskItemService.getRiskById(1L);
        assertNotNull(result);
    }

    @Test
    void testCreate() {
        Map<String, Object> result = riskItemService.create(new HashMap<>());
        assertNotNull(result);
    }
}
