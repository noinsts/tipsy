package ua.pp.tipsy.backend.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

public record CafeRequestDto(
        @NotBlank @Size(max = 255) String name,
        @NotBlank @Size(max = 2000) String description,
        @NotBlank @Size(max = 500) String address,
        @NotBlank @Pattern(regexp = "zona|doner", message = "type must be zona or doner") String type,
        @NotBlank @Size(max = 500) String photoUrl,
        @NotBlank @Size(max = 255) @Pattern(regexp = "[a-z0-9]+(?:-[a-z0-9]+)*", message = "slug must contain lowercase latin letters, digits and hyphens") String slug
) {}
