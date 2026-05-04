package com.internship.tool.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.thymeleaf.TemplateEngine;
import org.thymeleaf.context.Context;

import jakarta.mail.internet.MimeMessage;
import java.util.UUID;

@Service
@RequiredArgsConstructor
@Slf4j
public class EmailService {

    private final JavaMailSender mailSender;
    private final TemplateEngine templateEngine;

    @Value("${spring.mail.username: noreply@tool05.com}")
    private String fromEmail;

    @Value("${app.base-url: http://localhost:8080}")
    private String baseUrl;

    @Async
    public void sendRiskCreatedEmail(String toEmail, String riskTitle, UUID riskId) {
        try {
            Context context = new Context();
            context.setVariable("riskTitle", riskTitle);
            context.setVariable("riskId", riskId);
            context.setVariable("baseUrl", baseUrl);

            String htmlContent = templateEngine.process("email-template", context);

            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setFrom(fromEmail);
            helper.setTo(toEmail);
            helper.setSubject("New Risk Created: " + riskTitle);
            helper.setText(htmlContent, true);

            mailSender.send(message);
            log.info("Risk created email sent to {} for risk #{}", toEmail, riskId);
        } catch (Exception e) {
            log.error("Failed to send risk created email: {}", e.getMessage());
        }
    }

    @Async
    public void sendOverdueReminderEmail(String toEmail, String riskTitle, UUID riskId, String ownerName) {
        try {
            Context context = new Context();
            context.setVariable("riskTitle", riskTitle);
            context.setVariable("riskId", riskId);
            context.setVariable("ownerName", ownerName);
            context.setVariable("baseUrl", baseUrl);

            String htmlContent = templateEngine.process("email-template", context);

            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setFrom(fromEmail);
            helper.setTo(toEmail);
            helper.setSubject("OVERDUE: Risk requires attention - " + riskTitle);
            helper.setText(htmlContent, true);

            mailSender.send(message);
            log.info("Overdue reminder email sent to {} for risk #{}", toEmail, riskId);
        } catch (Exception e) {
            log.error("Failed to send overdue reminder email: {}", e.getMessage());
        }
    }

    @Async
    public void sendWeeklySummaryEmail(String toEmail, int totalRisks, int overdueCount, int highScoreCount) {
        try {
            Context context = new Context();
            context.setVariable("totalRisks", totalRisks);
            context.setVariable("overdueCount", overdueCount);
            context.setVariable("highScoreCount", highScoreCount);
            context.setVariable("baseUrl", baseUrl);

            String htmlContent = templateEngine.process("email-template", context);

            MimeMessage message = mailSender.createMimeMessage();
            MimeMessageHelper helper = new MimeMessageHelper(message, true, "UTF-8");

            helper.setFrom(fromEmail);
            helper.setTo(toEmail);
            helper.setSubject("Weekly Risk Summary - " + totalRisks + " total risks");
            helper.setText(htmlContent, true);

            mailSender.send(message);
            log.info("Weekly summary email sent to {}", toEmail);
        } catch (Exception e) {
            log.error("Failed to send weekly summary email: {}", e.getMessage());
        }
    }
}
