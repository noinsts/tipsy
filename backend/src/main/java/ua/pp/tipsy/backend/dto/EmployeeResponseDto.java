package ua.pp.tipsy.backend.dto;

import ua.pp.tipsy.backend.entity.Employee;

import java.time.LocalDate;

public record EmployeeResponseDto(
        Long id,
        String name,
        Long telegramId,
        LocalDate birthdayDate,
        String jarUrl,
        String photoUrl,
        boolean active
) {
    public static EmployeeResponseDto fromEntity(Employee employee) {
        return new EmployeeResponseDto(
                employee.getId(), employee.getName(), employee.getTelegramId(),
                employee.getBirthdayDate(), employee.getJarUrl(), employee.getPhotoUrl(),
                employee.isActive()
        );
    }
}
