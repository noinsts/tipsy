package ua.pp.tipsy.backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

import java.time.LocalDate;

public record EmployeeRequestDto(
        @NotBlank @Size(max = 255) String name,
        @NotNull @Positive Long telegramId,
        @NotNull LocalDate birthdayDate,
        @NotBlank @Size(max = 500) String jarUrl,
        @Size(max = 500) String photoUrl,
        boolean active
) {}
