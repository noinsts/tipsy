package ua.pp.tipsy.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import ua.pp.tipsy.backend.entity.Shift;

import java.time.LocalDate;
import java.util.List;

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
}
