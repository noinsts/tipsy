package ua.pp.tipsy.backend.dto;

import java.time.LocalDate;

public record BaristaResponseDto(Long id, String name, String photoUrl, String jarUrl, LocalDate birthdayDate) {}
