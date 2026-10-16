package ua.pp.tipsy.backend.service;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;
import ua.pp.tipsy.backend.dto.BaristaResponseDto;
import ua.pp.tipsy.backend.dto.CafeRequestDto;
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

    @Transactional(readOnly = true)
    public List<CafeResponseDto> getAllCafes() {
        return cafeRepository.findAll().stream()
                .map(CafeResponseDto::fromEntity)
                .toList();
    }

    @Transactional(readOnly = true)
    public CafeResponseDto getCafeById(Long id) {
        return CafeResponseDto.fromEntity(findCafe(id));
    }

    @Transactional
    public CafeResponseDto createCafe(CafeRequestDto request) {
        if (cafeRepository.existsBySlug(request.slug().trim())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Заклад зі таким slug вже існує");
        }
        Cafe cafe = new Cafe(
                request.name().trim(), request.description().trim(), request.address().trim(),
                request.type(), request.photoUrl().trim(), request.slug().trim()
        );
        return CafeResponseDto.fromEntity(cafeRepository.save(cafe));
    }

    @Transactional
    public CafeResponseDto updateCafe(Long id, CafeRequestDto request) {
        Cafe cafe = findCafe(id);
        String slug = request.slug().trim();
        if (cafeRepository.existsBySlugAndIdNot(slug, id)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Заклад зі таким slug вже існує");
        }
        cafe.update(
                request.name().trim(), request.description().trim(), request.address().trim(),
                request.type(), request.photoUrl().trim(), slug
        );
        return CafeResponseDto.fromEntity(cafeRepository.save(cafe));
    }

    @Transactional
    public void deleteCafe(Long id) {
        Cafe cafe = findCafe(id);
        if (shiftRepository.existsForCafe(id)) {
            throw new ResponseStatusException(
                    HttpStatus.CONFLICT,
                    "До закладу прив’язані зміни. Видалити його не можна."
            );
        }
        cafeRepository.delete(cafe);
    }

    public ShiftResponseDto getCafe(String slug) {
        Cafe cafe = cafeRepository.findBySlug(slug);
        if (cafe == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Заклад не знайдено");
        }
        CafeResponseDto cafeResponseDto = CafeResponseDto.fromEntity(cafe);

        List<Shift> shifts = shiftRepository.findShiftsByCafeSlugAndDate(slug, LocalDate.now());

        if (shifts.isEmpty()) {
            return new ShiftResponseDto(cafeResponseDto, null, null);
        }

        List<BaristaResponseDto> baristas = shifts.stream()
                .map(Shift::getEmployee)
                .map(e -> new BaristaResponseDto(e.getId(), e.getName(), e.getPhotoUrl(), e.getJarUrl(), e.getBirthdayDate()))
                .distinct()
                .toList();

        String jarUrl = shiftRepository
                .findFirstByCafeSlugAndShiftDateAndEmployeeActiveTrueOrderByIdAsc(slug, LocalDate.now())
                .map(shift -> shift.getEmployee().getJarUrl())
                .orElse(null);

        return new ShiftResponseDto(cafeResponseDto, java.util.Optional.of(baristas), jarUrl);
    }

    private Cafe findCafe(Long id) {
        return cafeRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Заклад не знайдено"));
    }
}
