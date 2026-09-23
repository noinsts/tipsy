package ua.pp.tipsy.backend.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.List;

/**
 * Для /api/bot/** перевіряє токен X-Bot-Token
 * Якщо токен вірний, то логінить запит як ROLE_BOT
 * Якщо ні - ігнорує і SecurityConfig дає 401
 */
public class BotTokenFilter extends OncePerRequestFilter {

    private static String HEADER = "X-Bot-Token";

    private final byte[] expected;

    public BotTokenFilter(String apiKey) {
        if (apiKey == null || apiKey.isBlank()) {
            throw new IllegalStateException("BOT_API_KEY must be set");
        }
        this.expected = apiKey.getBytes(StandardCharsets.UTF_8);
    }

    @Override
    protected boolean shouldNotFilter(HttpServletRequest request) {
        return !request.getServletPath().startsWith("/api/v1/bot");
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain
    ) throws ServletException, IOException {
        String provided = request.getHeader(HEADER);
        if (provided != null && MessageDigest.isEqual(provided.getBytes(StandardCharsets.UTF_8), expected)) {
            var auth = new UsernamePasswordAuthenticationToken(
                    "telegram-bot", null, List.of(new SimpleGrantedAuthority("ROLE_BOT"))
            );
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        filterChain.doFilter(request, response);
    }
}
