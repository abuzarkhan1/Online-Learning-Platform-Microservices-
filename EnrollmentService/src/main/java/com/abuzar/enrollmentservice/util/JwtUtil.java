package com.abuzar.enrollmentservice.util;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import javax.crypto.SecretKey;
import java.nio.charset.StandardCharsets;

@Slf4j
@Component
public class JwtUtil {

    @Value("${enrollment.jwt.secret}")
    private String jwtSecret;

    private SecretKey getSigningKey() {
        // Convert string to bytes using UTF-8 encoding (matching Node.js behavior)
        byte[] keyBytes = jwtSecret.getBytes(StandardCharsets.UTF_8);
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public Claims extractAllClaims(String token) {
        try {
            return Jwts.parserBuilder()
                    .setSigningKey(getSigningKey())
                    .build()
                    .parseClaimsJws(token)
                    .getBody();
        } catch (Exception e) {
            log.error("Failed to parse JWT token: {}", e.getMessage());
            throw e;
        }
    }

    public String extractUserId(String token) {
        Claims c = extractAllClaims(token);
        // Node.js JWT stores userId in 'id' claim
        Object id = c.get("id");
        if (id == null) {
            log.warn("No 'id' claim found in JWT. Available claims: {}", c.keySet());
        }
        return id != null ? id.toString() : null;
    }

    public String extractRole(String token) {
        Claims c = extractAllClaims(token);
        // Node.js JWT stores role in 'role' claim
        Object role = c.get("role");
        return role != null ? role.toString() : null;
    }
}