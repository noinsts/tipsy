package ua.pp.tipsy.backend.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import ua.pp.tipsy.backend.entity.Cafe;
import ua.pp.tipsy.backend.entity.Employee;
import ua.pp.tipsy.backend.entity.Shift;
import ua.pp.tipsy.backend.repository.CafeRepository;
import ua.pp.tipsy.backend.repository.EmployeeRepository;
import ua.pp.tipsy.backend.repository.ShiftRepository;

import java.time.LocalDate;

@Service
@RequiredArgsConstructor
public class ShiftService {

    private final ShiftRepository shiftRepository;
    private final CafeRepository cafeRepository;
    private final EmployeeRepository employeeRepository;

    public Shift openShift(Long cafeId, Long employeeId) {
        LocalDate date = LocalDate.now();

        Cafe cafe = cafeRepository.findById(cafeId)
                .orElseThrow(() -> new IllegalArgumentException("Неможливо знайти кав'ярню"));

        Employee employee = employeeRepository.findById(employeeId)
                .orElseThrow(() -> new IllegalArgumentException("Неможливо знайти працівника"));

        Shift shift = new Shift(cafe, employee, date);
        return shiftRepository.save(shift);
    }

    public void deleteShift(Long shiftId) {
        if (!shiftRepository.existsById(shiftId)) {
            return;
        }
        shiftRepository.deleteById(shiftId);
    }
}
