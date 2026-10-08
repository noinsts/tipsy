package ua.pp.tipsy.backend.controller;

import lombok.RequiredArgsConstructor;
import org.apache.coyote.Response;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityReturnValueHandler;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.entity.Shift;
import ua.pp.tipsy.backend.service.EmployeeService;
import ua.pp.tipsy.backend.service.ImageStorageService;
import ua.pp.tipsy.backend.service.ShiftService;

import java.io.IOException;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/bot")
@RequiredArgsConstructor
public class BotController {

    private final EmployeeService employeeService;
    private final ShiftService shiftService;
    private final ImageStorageService imageStorageService;

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

    @PostMapping(value = "/images/", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Map<String, String> upload(@RequestParam MultipartFile file) throws IOException {
        return Map.of("url", imageStorageService.save(file));
    }

    @DeleteMapping("/images/")
    public ResponseEntity<Void> deleteByUrl(@RequestParam String url) throws IOException {
        return imageStorageService.deleteByUrl(url)
                ? ResponseEntity.noContent().build()
                : ResponseEntity.notFound().build();
    }
}
