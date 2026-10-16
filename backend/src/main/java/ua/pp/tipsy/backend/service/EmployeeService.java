package ua.pp.tipsy.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.dto.EmployeeRequestDto;
import ua.pp.tipsy.backend.dto.EmployeeResponseDto;
import ua.pp.tipsy.backend.entity.Employee;
import ua.pp.tipsy.backend.repository.EmployeeRepository;
import ua.pp.tipsy.backend.repository.ShiftRepository;

import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class EmployeeService {

    private final EmployeeRepository employeeRepository;
    private final ShiftRepository shiftRepository;

    public Optional<BaristaResponseDto> getBaristaById(Long telegramId) {
        return employeeRepository.findBaristaByTelegramId(telegramId);
    }

    @Transactional(readOnly = true)
    public List<EmployeeResponseDto> getAllEmployees() {
        return employeeRepository.findAll().stream()
                .map(EmployeeResponseDto::fromEntity)
                .toList();
    }

    @Transactional(readOnly = true)
    public EmployeeResponseDto getEmployee(Long id) {
        return EmployeeResponseDto.fromEntity(findEmployee(id));
    }

    @Transactional
    public EmployeeResponseDto createEmployee(EmployeeRequestDto request) {
        if (employeeRepository.existsByTelegramId(request.telegramId())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Працівник з таким Telegram ID вже існує");
        }

        Employee employee = new Employee(
                request.name().trim(), request.telegramId(), request.birthdayDate(),
                request.jarUrl().trim(), normalizeOptional(request.photoUrl()), request.active()
        );
        return EmployeeResponseDto.fromEntity(employeeRepository.save(employee));
    }

    @Transactional
    public EmployeeResponseDto updateEmployee(Long id, EmployeeRequestDto request) {
        Employee employee = findEmployee(id);
        if (employeeRepository.existsByTelegramIdAndIdNot(request.telegramId(), id)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Працівник з таким Telegram ID вже існує");
        }

        employee.update(
                request.name().trim(), request.telegramId(), request.birthdayDate(),
                request.jarUrl().trim(), normalizeOptional(request.photoUrl()), request.active()
        );
        return EmployeeResponseDto.fromEntity(employeeRepository.save(employee));
    }

    @Transactional
    public void deleteEmployee(Long id) {
        Employee employee = findEmployee(id);
        if (shiftRepository.existsForEmployee(id)) {
            throw new ResponseStatusException(
                    HttpStatus.CONFLICT,
                    "До працівника прив’язані зміни. Видалити його не можна."
            );
        }
        employeeRepository.delete(employee);
    }

    private Employee findEmployee(Long id) {
        return employeeRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Працівника не знайдено"));
    }

    private String normalizeOptional(String value) {
        return value == null || value.isBlank() ? null : value.trim();
    }
}
