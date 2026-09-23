package ua.pp.tipsy.backend.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;

import java.time.LocalDate;

@Entity
@Getter
@Table(name = "shifts")
@NoArgsConstructor
public class Shift {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "cafe_id")
    private Cafe cafe;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "employer_id")
    private Employee employee;

    @Column(name = "shift_date", nullable = false)
    private LocalDate shiftDate;

    public Shift(Cafe cafe, Employee employee, LocalDate shiftDate) {
        this.cafe = cafe;
        this.employee = employee;
        this.shiftDate = shiftDate;
    }
}
