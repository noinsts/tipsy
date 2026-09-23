package ua.pp.tipsy.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.repository.EmployeeRepository;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class EmployeeService {

    private final EmployeeRepository employeeRepository;

    public Optional<BaristaResponseDto> getBaristaById(Long telegramId) {
        return employeeRepository.findBaristaByTelegramId(telegramId);
    }
}
