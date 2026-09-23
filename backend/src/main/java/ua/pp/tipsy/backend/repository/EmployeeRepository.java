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
            e.photo_url,
            e.jar_url             
        )
        FROM Employee e
        WHERE e.telegram_id = :telegramId
    """)
    Optional<BaristaResponseDto> findBaristaByTelegramId(@Param("telegramId") Long telegram_id);
}
