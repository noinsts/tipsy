package ua.pp.tipsy.backend.controller;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import ua.pp.tipsy.backend.dto.CafeRequestDto;
import ua.pp.tipsy.backend.dto.CafeResponseDto;
import ua.pp.tipsy.backend.dto.EmployeeRequestDto;
import ua.pp.tipsy.backend.dto.EmployeeResponseDto;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.entity.Shift;
import ua.pp.tipsy.backend.service.CafeService;
import ua.pp.tipsy.backend.service.EmployeeService;
import ua.pp.tipsy.backend.service.ImageStorageService;
import ua.pp.tipsy.backend.service.ShiftService;

import java.io.IOException;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/bot")
@RequiredArgsConstructor
public class BotController {

    private final EmployeeService employeeService;
    private final CafeService cafeService;
    private final ShiftService shiftService;
    private final ImageStorageService imageStorageService;

    // Employees CRUD
    @GetMapping({"/employees", "/employees/"})
    public List<EmployeeResponseDto> getEmployees() {
        return employeeService.getAllEmployees();
    }

    @GetMapping({"/employees/{id}", "/employees/{id}/"})
    public EmployeeResponseDto getEmployee(@PathVariable Long id) {
        return employeeService.getEmployee(id);
    }

    @PostMapping({"/employees", "/employees/"})
    public ResponseEntity<EmployeeResponseDto> createEmployee(@Valid @RequestBody EmployeeRequestDto request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(employeeService.createEmployee(request));
    }

    @PutMapping({"/employees/{id}", "/employees/{id}/"})
    public EmployeeResponseDto updateEmployee(
            @PathVariable Long id,
            @Valid @RequestBody EmployeeRequestDto request
    ) {
        return employeeService.updateEmployee(id, request);
    }

    @DeleteMapping({"/employees/{id}", "/employees/{id}/"})
    public ResponseEntity<Void> deleteEmployee(@PathVariable Long id) {
        employeeService.deleteEmployee(id);
        return ResponseEntity.noContent().build();
    }

    // Cafes CRUD
    @GetMapping({"/cafes", "/cafes/"})
    public List<CafeResponseDto> getCafes() {
        return cafeService.getAllCafes();
    }

    @GetMapping({"/cafes/{id}", "/cafes/{id}/"})
    public CafeResponseDto getCafe(@PathVariable Long id) {
        return cafeService.getCafeById(id);
    }

    @PostMapping({"/cafes", "/cafes/"})
    public ResponseEntity<CafeResponseDto> createCafe(@Valid @RequestBody CafeRequestDto request) {
        return ResponseEntity.status(HttpStatus.CREATED).body(cafeService.createCafe(request));
    }

    @PutMapping({"/cafes/{id}", "/cafes/{id}/"})
    public CafeResponseDto updateCafe(@PathVariable Long id, @Valid @RequestBody CafeRequestDto request) {
        return cafeService.updateCafe(id, request);
    }

    @DeleteMapping({"/cafes/{id}", "/cafes/{id}/"})
    public ResponseEntity<Void> deleteCafe(@PathVariable Long id) {
        cafeService.deleteCafe(id);
        return ResponseEntity.noContent().build();
    }

    // Employee bot endpoints
    @GetMapping({"/barista/{telegramId}", "/barista/{telegramId}/"})
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

    @PostMapping(value = {"/images", "/images/"}, consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public Map<String, String> upload(@RequestParam MultipartFile file) throws IOException {
        return Map.of("url", imageStorageService.save(file));
    }

    @DeleteMapping({"/images", "/images/"})
    public ResponseEntity<Void> deleteByUrl(@RequestParam String url) throws IOException {
        return imageStorageService.deleteByUrl(url)
                ? ResponseEntity.noContent().build()
                : ResponseEntity.notFound().build();
    }
}
