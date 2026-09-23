package ua.pp.tipsy.backend.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import ua.pp.tipsy.backend.entity.Cafe;

@Repository
public interface CafeRepository extends JpaRepository<Cafe, Long> {

    @Query("""
        SELECT c FROM Cafe c WHERE c.slug = :slug
    """)
    Cafe findBySlug(@Param("slug") String slug);
}
