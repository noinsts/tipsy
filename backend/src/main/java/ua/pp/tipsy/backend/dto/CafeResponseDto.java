package ua.pp.tipsy.backend.dto;

import ua.pp.tipsy.backend.entity.Cafe;

public record CafeResponseDto(
    Long id,
    String name,
    String description,
    String address,
    String type,
    String photoUrl,
    String slug
) {
    public static CafeResponseDto fromEntity(Cafe cafe) {
        if (cafe == null) {
            return null;
        }
        return new CafeResponseDto(
                cafe.getId(),
                cafe.getName(),
                cafe.getDescription(),
                cafe.getAddress(),
                cafe.getType(),
                cafe.getPhotoUrl(),
                cafe.getSlug()
        );
    }
}
