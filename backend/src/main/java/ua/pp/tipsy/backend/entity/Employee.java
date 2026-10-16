package ua.pp.tipsy.backend.entity;

import jakarta.persistence.*;
import lombok.Getter;

import java.time.LocalDate;

@Entity
@Getter
@Table(name = "employees")
public class Employee {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(name = "telegram_id", nullable = false, unique = true)
    private Long telegramId;

    @Column(name = "birthday_date", nullable = false)
    private LocalDate birthdayDate;

    @Column(name = "jar_url", nullable = false, length = 500)
    private String jarUrl;

    @Column(name = "photo_url", length = 500)
    private String photoUrl;

    @Column(nullable = false)
    private boolean active;

    protected Employee() {}

    public Employee(String name, Long telegramId, LocalDate birthdayDate,
                    String jarUrl, String photoUrl, boolean active) {
        this.name = name;
        this.telegramId = telegramId;
        this.birthdayDate = birthdayDate;
        this.jarUrl = jarUrl;
        this.photoUrl = photoUrl;
        this.active = active;
    }

    public void update(String name, Long telegramId, LocalDate birthdayDate,
                       String jarUrl, String photoUrl, boolean active) {
        this.name = name;
        this.telegramId = telegramId;
        this.birthdayDate = birthdayDate;
        this.jarUrl = jarUrl;
        this.photoUrl = photoUrl;
        this.active = active;
    }
}
