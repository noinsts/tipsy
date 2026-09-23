package ua.pp.tipsy.backend.service;

import org.springframework.stereotype.Service;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.dto.CafeResponseDto;
import ua.pp.tipsy.backend.dto.ShiftResponseDto;
import ua.pp.tipsy.backend.entity.Cafe;
import ua.pp.tipsy.backend.entity.Shift;
import ua.pp.tipsy.backend.repository.CafeRepository;
import ua.pp.tipsy.backend.repository.ShiftRepository;

import java.time.LocalDate;
import java.util.List;

@Service
public class CafeService {

    private final CafeRepository cafeRepository;
    private final ShiftRepository shiftRepository;

    public CafeService(CafeRepository cafeRepository, ShiftRepository shiftRepository) {
        this.cafeRepository = cafeRepository;
        this.shiftRepository = shiftRepository;
    }

    public List<CafeResponseDto> getAllCafes() {
        return cafeRepository.findAll().stream()
                .map(cafe -> new CafeResponseDto(cafe.getId(), cafe.getName(), cafe.getSlug()))
                .toList();
    }

    public ShiftResponseDto getCafe(String slug) {
        Cafe cafe = cafeRepository.findBySlug(slug);
        List<Shift> shifts = shiftRepository.findShiftsByCafeSlugAndDate(slug, LocalDate.now());
        if (shifts.isEmpty()) {
            return new ShiftResponseDto(cafe.getName(), null);
        }
        List<BaristaResponseDto> baristas = shifts.stream()
                .map(Shift::getEmployee)
                .map(e -> new BaristaResponseDto(e.getId(), e.getName(), e.getPhoto_url(), e.getJar_url()))
                .distinct()
                .toList();

        return new ShiftResponseDto(cafe.getName(), java.util.Optional.of(baristas));
    }
}
