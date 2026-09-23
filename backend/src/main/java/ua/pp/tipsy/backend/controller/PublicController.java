package ua.pp.tipsy.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ua.pp.tipsy.backend.dto.CafeResponseDto;
import ua.pp.tipsy.backend.dto.ShiftResponseDto;
import ua.pp.tipsy.backend.service.CafeService;

import java.util.List;

@RestController
@RequestMapping("/api/v1/public")
@CrossOrigin(origins = {"http://localhost:5173", "http://127.0.0.1:5173"})
public class PublicController {

    private final CafeService cafeService;

    public PublicController(CafeService cafeService) {
        this.cafeService = cafeService;
    }

    @GetMapping({"/cafes", "/cafes/"})
    public ResponseEntity<List<CafeResponseDto>> getAllCafes() {
        return ResponseEntity.ok(cafeService.getAllCafes());
    }

    @GetMapping({"/cafe/{slug}", "/cafe/{slug}/"})
    public ResponseEntity<ShiftResponseDto> getCafe(@PathVariable String slug) {
        return ResponseEntity.ok(cafeService.getCafe(slug));
    }
}
