package ua.pp.tipsy.backend.entity;

import jakarta.persistence.*;
import lombok.Getter;

@Entity
@Getter
@Table(name = "employees")
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private Long telegram_id;

    @Column(nullable = false, length = 500)
    private String jar_url;

    @Column(nullable = true, length = 500)
    private String photo_url;

    @Column(nullable = false)
    private boolean active;

    protected Employee() {}
}
