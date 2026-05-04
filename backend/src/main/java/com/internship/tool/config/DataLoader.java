package com.internship.tool.config;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

@Component
@Profile("!test")
@RequiredArgsConstructor
@Slf4j
public class DataLoader implements CommandLineRunner {

    @Override
    public void run(String... args) {
        log.info("DataLoader executed, but logic removed due to missing dependencies.");
    }
}
