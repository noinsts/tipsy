package ua.pp.tipsy.backend.service;

import org.apache.tomcat.util.http.fileupload.MultipartStream;
import org.hibernate.type.StandardBasicTypes;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Map;
import java.util.UUID;

@Service
public class ImageStorageService {

    private static final Map<String, String> ALLOWED = Map.of(
            "image/jpeg", "jpg",
            "image/png", "png",
            "image/webp", "webp"
    );

    private final Path root;
    private final String baseUrl;

    public ImageStorageService(
            @Value("${app.upload-dir}") String uploadDir,
            @Value("${app.public-base-url}") String baseUrl
    ) throws IOException {
        this.root = Paths.get(uploadDir).toAbsolutePath().normalize();
        this.baseUrl = baseUrl.replaceAll("/+$", "") + "/api/v1/public/static/images/";
        Files.createDirectories(root);
    }

    public String save(MultipartFile file) throws IOException {
        if (file.isEmpty()) {
            throw new IllegalArgumentException("Порожній файл");
        }
        String ext = ALLOWED.get(file.getContentType());
        if (ext == null) {
            throw new IllegalArgumentException("Дозволені лише jpg, png, webp");
        }
        String filename = UUID.randomUUID() + "." + ext;
        Files.copy(file.getInputStream(), root.resolve(filename), StandardCopyOption.REPLACE_EXISTING);
        return baseUrl + filename;
    }

    public boolean deleteByUrl(String url) throws IOException {
        if (!url.startsWith(baseUrl)) {
            throw new IllegalArgumentException("Url не належить цьому сервісу");
        }
        // Delete by filename
        Path target = root.resolve(url.substring(baseUrl.length())).normalize();
        if (!target.startsWith(root)) {
            throw new IllegalArgumentException("Некоректне ім'я файлу");
        }
        return Files.deleteIfExists(target);
    }
}
