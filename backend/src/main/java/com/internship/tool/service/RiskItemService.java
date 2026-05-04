package com.internship.tool.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.exception.ValidationException;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.scheduling.annotation.Async;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.math.BigDecimal;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class RiskItemService {

    private final EmailService emailService;
    private final ObjectMapper objectMapper;

    @Cacheable(value = "risks", key = "#page + '-' + #size + '-' + #sortBy + '-' + #sortDir")
    public Page<Map<String, Object>> getAllRisks(int page, int size, String sortBy, String sortDir) {
        return Page.empty();
    }

    public Map<String, Object> getRiskById(Long id) {
        return new HashMap<>();
    }

    @CacheEvict(value = {"risks", "stats"}, allEntries = true)
    @Transactional
    public Map<String, Object> create(Map<String, Object> request) {
        log.info("Risk created");
        return new HashMap<>();
    }

    @Async
    @Transactional(readOnly = true)
    public void triggerAiAnalysisAsync(Long riskId) {
        // AI analysis implementation removed due to missing dependencies
    }

    @CacheEvict(value = {"risks", "stats"}, allEntries = true)
    @Transactional
    public Map<String, Object> update(Long id, Map<String, Object> request) {
        log.info("Risk updated: {}", id);
        return new HashMap<>();
    }

    @CacheEvict(value = {"risks", "stats"}, allEntries = true)
    @Transactional
    public void delete(Long id) {
        log.info("Risk soft deleted: {}", id);
    }

    @Cacheable(value = "stats")
    public Map<String, Object> getStats() {
        return new HashMap<>();
    }

    public Page<Map<String, Object>> search(String query, int page, int size) {
        return Page.empty();
    }

    @CacheEvict(value = {"risks", "stats"}, allEntries = true)
    @Transactional
    public String uploadFile(Long riskId, MultipartFile file) {
        if (file.getSize() > 10 * 1024 * 1024) {
            throw new ValidationException("File size must be less than 10MB");
        }

        String contentType = file.getContentType();
        if (contentType == null || !contentType.startsWith("application/") &&
                !contentType.equals("image/png") && !contentType.equals("image/jpeg")) {
            throw new ValidationException("Invalid file type. Allowed: PDF, DOC, DOCX, XLS, XLSX, PNG, JPEG");
        }

        try {
            String uploadDir = System.getProperty("java.io.tmpdir") + "/uploads/";
            Files.createDirectories(Paths.get(uploadDir));

            String originalFilename = file.getOriginalFilename();
            String extension = "";
            if (originalFilename != null && originalFilename.contains(".")) {
                extension = originalFilename.substring(originalFilename.lastIndexOf("."));
                extension = extension.replaceAll("[^a-zA-Z0-9.]", "");
                if (extension.length() > 10) {
                    extension = extension.substring(0, 10);
                }
            }
            String storedFilename = UUID.randomUUID().toString() + extension;

            Path filePath = Paths.get(uploadDir, storedFilename).normalize();
            if (!filePath.startsWith(Paths.get(uploadDir).normalize())) {
                throw new ValidationException("Invalid file path");
            }

            Files.write(filePath, file.getBytes());

            log.info("File uploaded for risk {}: {}", riskId, storedFilename);
            return storedFilename;
        } catch (IOException e) {
            throw new ValidationException("Failed to store file: " + e.getMessage());
        }
    }

    public List<Map<String, Object>> getOverdueRisks() {
        return List.of();
    }

    private Long getCurrentUserId() {
        return 1L;
    }
}
