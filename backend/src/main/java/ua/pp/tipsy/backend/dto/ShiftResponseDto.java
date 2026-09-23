package ua.pp.tipsy.backend.dto;

import java.util.List;
import java.util.Optional;

public record ShiftResponseDto(String cafeName, Optional<List<BaristaResponseDto>> baristas) {}
