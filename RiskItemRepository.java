package com.internship.tool.repository;

import com.internship.tool.entity.RiskCategory;
import com.internship.tool.entity.RiskItem;
import com.internship.tool.entity.RiskStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface RiskItemRepository extends JpaRepository<RiskItem, Long>, JpaSpecificationExecutor<RiskItem> {

    Page<RiskItem> findByDeletedFalse(Pageable pageable);

    Optional<RiskItem> findByIdAndDeletedFalse(Long id);

    @Query("SELECT r FROM RiskItem r WHERE r.deleted = false AND " +
           "(LOWER(r.title) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
           "LOWER(r.description) LIKE LOWER(CONCAT('%', :q, '%')) OR " +
           "LOWER(r.owner) LIKE LOWER(CONCAT('%', :q, '%')))")
    Page<RiskItem> search(@Param("q") String query, Pageable pageable);

    @Query("SELECT r FROM RiskItem r WHERE r.deleted = false AND r.status = :status")
    Page<RiskItem> findByStatus(@Param("status") RiskStatus status, Pageable pageable);

    @Query("SELECT r FROM RiskItem r WHERE r.deleted = false AND r.category = :category")
    Page<RiskItem> findByCategory(@Param("category") RiskCategory category, Pageable pageable);

    @Query("SELECT r FROM RiskItem r WHERE r.deleted = false AND r.dueDate < :date AND r.status NOT IN ('LOW')")
    List<RiskItem> findOverdueRisks(@Param("date") LocalDate date);

    @Query("SELECT COUNT(r) FROM RiskItem r WHERE r.deleted = false AND r.score >= 7")
    long countHighScoreRisks();

    @Query("SELECT COUNT(r) FROM RiskItem r WHERE r.deleted = false AND r.dueDate < :date AND r.status != 'CRITICAL'")
    long countOverdueRisks(@Param("date") LocalDate date);

    @Query("SELECT COUNT(r) FROM RiskItem r WHERE r.deleted = false AND r.status = 'RESOLVED' AND r.updatedAt >= :startOfMonth")
    long countResolvedThisMonth(@Param("startOfMonth") LocalDateTime startOfMonth);

    @Query("SELECT r.category, COUNT(r) FROM RiskItem r WHERE r.deleted = false GROUP BY r.category")
    List<Object[]> countByCategory();

    @Query("SELECT r.status, COUNT(r) FROM RiskItem r WHERE r.deleted = false GROUP BY r.status")
    List<Object[]> countByStatus();
}
