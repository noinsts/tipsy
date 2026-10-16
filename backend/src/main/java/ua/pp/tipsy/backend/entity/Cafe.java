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

    @Column(nullable = false, length = 2000)
    private String description;

    @Column(nullable = false, length = 500)
    private String address;

    @Column(nullable = false)
    private String type; // zona / doner

    @Column(nullable = false, length = 500)
    private String photoUrl;

    @Column(nullable = false, unique = true)
    private String slug;

    protected Cafe() {}

    public Cafe(String name, String description, String address,
                String type, String photoUrl, String slug) {
        this.name = name;
        this.description = description;
        this.address = address;
        this.type = type;
        this.photoUrl = photoUrl;
        this.slug = slug;
    }

    public void update(String name, String description, String address,
                       String type, String photoUrl, String slug) {
        this.name = name;
        this.description = description;
        this.address = address;
        this.type = type;
        this.photoUrl = photoUrl;
        this.slug = slug;
    }
}
