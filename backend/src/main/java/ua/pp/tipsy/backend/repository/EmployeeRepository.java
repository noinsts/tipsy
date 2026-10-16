package ua.pp.tipsy.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.entity.Employee;

import java.util.Optional;

public interface EmployeeRepository extends JpaRepository<Employee, Long> {

    @Query("""
        SELECT new ua.pp.tipsy.backend.dto.BaristaResponseDto(
            e.id,
            e.name,
            e.photoUrl,
            e.jarUrl,
            e.birthdayDate
        )
        FROM Employee e
        WHERE e.telegramId = :telegramId AND e.active = true
    """)
    Optional<BaristaResponseDto> findBaristaByTelegramId(@Param("telegramId") Long telegramId);

    boolean existsByTelegramId(Long telegramId);

    boolean existsByTelegramIdAndIdNot(Long telegramId, Long id);
}
