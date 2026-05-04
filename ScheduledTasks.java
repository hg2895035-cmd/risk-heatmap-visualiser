package com.internship.tool.scheduler;

import com.internship.tool.entity.RiskItem;
import com.internship.tool.entity.RiskStatus;
import com.internship.tool.repository.AppUserRepository;
import com.internship.tool.repository.RiskItemRepository;
import com.internship.tool.service.EmailService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.util.List;

@Component
@RequiredArgsConstructor
@Slf4j
public class ScheduledTasks {

    private final RiskItemRepository riskItemRepository;
    private final AppUserRepository appUserRepository;
    private final EmailService emailService;

    @Scheduled(cron = "0 0 8 * * *")
    public void dailyOverdueReminder() {
        log.info("Running daily overdue reminder task");
        List<RiskItem> overdueRisks = riskItemRepository.findOverdueRisks(LocalDate.now());

        for (RiskItem risk : overdueRisks) {
            if (risk.getOwner() != null && !risk.getOwner().isEmpty()) {
                emailService.sendOverdueReminderEmail(
                        risk.getOwner() + "@company.com",
                        risk.getTitle(),
                        risk.getId(),
                        risk.getOwner()
                );
            }
        }
        log.info("Sent {} overdue reminders", overdueRisks.size());
    }

    @Scheduled(cron = "0 0 8 * * MON")
    public void weeklySummary() {
        log.info("Running weekly summary task");
        long totalRisks = riskItemRepository.count();
        long overdueCount = riskItemRepository.countOverdueRisks(LocalDate.now());
        long highScoreCount = riskItemRepository.countHighScoreRisks();

        appUserRepository.findAll().forEach(user -> {
            emailService.sendWeeklySummaryEmail(
                    user.getEmail(),
                    (int) totalRisks,
                    (int) overdueCount,
                    (int) highScoreCount
            );
        });
        log.info("Sent weekly summary to {} users", appUserRepository.count());
    }

    @Scheduled(cron = "0 0 8 * * *")
    public void deadlineAlert() {
        log.info("Running 7-day deadline alert task");
        LocalDate alertDate = LocalDate.now().plusDays(7);

        List<RiskItem> upcomingDeadlines = riskItemRepository.findByDeletedFalse(
                        org.springframework.data.domain.Pageable.unpaged())
                .filter(r -> r.getDueDate() != null)
                .filter(r -> r.getDueDate().equals(alertDate))
                .toList();

        for (RiskItem risk : upcomingDeadlines) {
            if (risk.getOwner() != null) {
                emailService.sendOverdueReminderEmail(
                        risk.getOwner() + "@company.com",
                        risk.getTitle(),
                        risk.getId(),
                        risk.getOwner()
                );
            }
        }
        log.info("Sent {} deadline alerts", upcomingDeadlines.size());
    }
}
