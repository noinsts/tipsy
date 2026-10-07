package ua.pp.tipsy.backend.dto;

import java.util.List;
import java.util.Optional;

public record ShiftResponseDto(CafeResponseDto cafe, Optional<List<BaristaResponseDto>> baristas, String jarUrl) {}
