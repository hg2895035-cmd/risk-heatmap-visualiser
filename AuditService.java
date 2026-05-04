package com.internship.tool.service;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Aspect
@Component
@RequiredArgsConstructor
@Slf4j
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    @Around("execution(* com.internship.tool.service.RiskItemService.create(..)) || " +
            "execution(* com.internship.tool.service.RiskItemService.update(..)) || " +
            "execution(* com.internship.tool.service.RiskItemService.delete(..))")
    public Object auditRiskOperations(ProceedingJoinPoint joinPoint) throws Throwable {
        String methodName = joinPoint.getSignature().getName();
        Object[] args = joinPoint.getArgs();

        Long userId = getCurrentUserId();
        String action = methodName.equals("delete") ? "DELETE" : methodName.equals("create") ? "CREATE" : "UPDATE";

        Object oldValue = null;
        if (methodName.equals("update") && args.length > 0 && args[0] instanceof Long) {
            oldValue = getOldRiskJson((Long) args[0]);
        }

        Object result = joinPoint.proceed();

        String newValue = null;
        if (result != null) {
            newValue = result.toString();
        }

        AuditLog auditLog = AuditLog.builder()
                .entityType("RiskItem")
                .entityId(extractEntityId(result))
                .action(action)
                .oldValue(oldValue != null ? oldValue.toString() : null)
                .newValue(newValue)
                .changedBy(userId)
                .changedAt(LocalDateTime.now())
                .build();

        auditLogRepository.save(auditLog);
        log.debug("Audit log created: {} on RiskItem #{}", action, auditLog.getEntityId());

        return result;
    }

    private Long getCurrentUserId() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof org.springframework.security.core.userdetails.User) {
            String email = ((org.springframework.security.core.userdetails.User) auth.getPrincipal()).getUsername();
            return null;
        }
        return null;
    }

    private Object getOldRiskJson(Long id) {
        return "{ \"id\": " + id + " }";
    }

    private Long extractEntityId(Object result) {
        if (result == null) return null;
        if (result instanceof com.internship.tool.entity.RiskItem) {
            return ((com.internship.tool.entity.RiskItem) result).getId();
        }
        return null;
    }
}
