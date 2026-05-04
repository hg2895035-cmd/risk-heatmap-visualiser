package com.internship.tool.repository;

import com.internship.tool.entity.Risk;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface RiskRepository extends JpaRepository<Risk, UUID> {
}
