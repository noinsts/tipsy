package ua.pp.tipsy.backend.entity;

import jakarta.persistence.*;
import lombok.Getter;

@Entity
@Getter
@Table(name = "cafes")
public class Cafe {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private String description;

    @Column(nullable = false)
    private String type; // zona / doner

    @Column(nullable = false)
    private String photoUrl;

    @Column(nullable = false, unique = true)
    private String slug;

    protected Cafe() {}

}
