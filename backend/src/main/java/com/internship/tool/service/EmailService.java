package com.internship.tool.service;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class EmailService {

    private final JavaMailSender mailSender;

    public void sendCreationEmail(String to, String riskTitle) {
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(to);
            message.setSubject("New Risk Created: " + riskTitle);
            message.setText("A new risk titled '" + riskTitle + "' has been created and assigned to you.");
            mailSender.send(message);
            log.info("Creation email sent successfully to {}", to);
        } catch (Exception e) {
            log.error("Failed to send creation email to {}", to, e);
        }
    }

    public void sendOverdueEmail(String to, String riskTitle) {
        try {
            SimpleMailMessage message = new SimpleMailMessage();
            message.setTo(to);
            message.setSubject("Risk Overdue: " + riskTitle);
            message.setText("The risk titled '" + riskTitle + "' is overdue. Please take action immediately.");
            mailSender.send(message);
            log.info("Overdue email sent successfully to {}", to);
        } catch (Exception e) {
            log.error("Failed to send overdue email to {}", to, e);
        }
    }
}
