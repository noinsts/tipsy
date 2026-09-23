package ua.pp.tipsy.backend.controller;

import lombok.RequiredArgsConstructor;
import org.apache.coyote.Response;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityReturnValueHandler;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.entity.Shift;
import ua.pp.tipsy.backend.service.EmployeeService;
import ua.pp.tipsy.backend.service.ShiftService;

@RestController
@RequestMapping("/api/v1/bot")
@RequiredArgsConstructor
public class BotController {

    private final EmployeeService employeeService;
    private final ShiftService shiftService;

    @GetMapping({"/barista/{telegramId}", "barista/{telegramId}/"})
    public ResponseEntity<BaristaResponseDto> getBaristaByTelegramId(@PathVariable Long telegramId) {
        return employeeService.getBaristaById(telegramId)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping({"/shift/open", "/shift/open/"})
    public ResponseEntity<Long> openShift(@RequestParam Long cafeId, @RequestParam Long employeeId) {
        Shift shift = shiftService.openShift(cafeId, employeeId);
        return ResponseEntity.ok(shift.getId());
    }

    @DeleteMapping({"/shift/{id}", "/shift/{id}/"})
    public ResponseEntity<Void> deleteShift(@PathVariable Long id) {
        shiftService.deleteShift(id);
        return ResponseEntity.noContent().build();
    }
}
