package ua.pp.tipsy.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import ua.pp.tipsy.backend.entity.Shift;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface ShiftRepository extends JpaRepository<Shift, Long> {

    @Query("""
        SELECT DISTINCT s FROM Shift s
            JOIN FETCH s.cafe c
            JOIN FETCH s.employee e
            WHERE c.slug = :slug
                AND s.shiftDate = :date
                AND e.active = true
    """)
    List<Shift> findShiftsByCafeSlugAndDate(@Param("slug") String slug, @Param("date") LocalDate date);

    Optional<Shift> findFirstByCafeSlugAndShiftDateAndEmployeeActiveTrueOrderByIdAsc(String slug, LocalDate date);

    @Query("SELECT CASE WHEN COUNT(s) > 0 THEN true ELSE false END FROM Shift s WHERE s.employee.id = :employeeId")
    boolean existsForEmployee(@Param("employeeId") Long employeeId);

    @Query("SELECT CASE WHEN COUNT(s) > 0 THEN true ELSE false END FROM Shift s WHERE s.cafe.id = :cafeId")
    boolean existsForCafe(@Param("cafeId") Long cafeId);
}
