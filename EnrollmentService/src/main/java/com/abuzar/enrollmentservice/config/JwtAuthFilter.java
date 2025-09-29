package com.abuzar.enrollmentservice.config;

import com.abuzar.enrollmentservice.util.JwtUtil;
import io.jsonwebtoken.Claims;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.List;

@Slf4j
@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtUtil jwtUtil;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {

        log.debug("Processing request: {} {}", request.getMethod(), request.getRequestURI());

        final String header = request.getHeader(HttpHeaders.AUTHORIZATION);

        if (header == null || !header.startsWith("Bearer ")) {
            log.debug("No Bearer token found in Authorization header");
            filterChain.doFilter(request, response);
            return;
        }

        final String token = header.substring(7);
        log.debug("Extracted JWT token: {}...", token.substring(0, Math.min(20, token.length())));

        try {
            Claims claims = jwtUtil.extractAllClaims(token);
            String userId = jwtUtil.extractUserId(token);
            String role = jwtUtil.extractRole(token);

            log.info("JWT validated successfully - userId: {}, role: {}", userId, role);

            if (userId != null) {
                String roleName = role != null ? role.toUpperCase() : "USER";
                SimpleGrantedAuthority auth = new SimpleGrantedAuthority("ROLE_" + roleName);
                UsernamePasswordAuthenticationToken authentication =
                        new UsernamePasswordAuthenticationToken(userId, null, List.of(auth));
                SecurityContextHolder.getContext().setAuthentication(authentication);
                log.info("Authentication set successfully for user: {} with role: ROLE_{}", userId, roleName);
            } else {
                log.warn("userId is null, authentication not set");
            }
        } catch (Exception ex) {
            log.error("JWT validation failed: {} - {}", ex.getClass().getSimpleName(), ex.getMessage());
        }

        filterChain.doFilter(request, response);
    }
}