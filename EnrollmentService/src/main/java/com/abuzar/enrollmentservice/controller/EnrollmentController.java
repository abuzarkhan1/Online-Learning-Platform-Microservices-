package com.abuzar.enrollmentservice.controller;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import com.abuzar.enrollmentservice.dto.EnrollmentRequest;
import com.abuzar.enrollmentservice.models.Certificate;
import com.abuzar.enrollmentservice.models.Enrollment;
import com.abuzar.enrollmentservice.models.Progress;
import com.abuzar.enrollmentservice.service.EnrollmentService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.*;

import java.util.List;
@Tag(name = "Enrollment Management", description = "Endpoints for enrollment, progress tracking, and certificates")
@Slf4j
@RestController
@RequestMapping("/api/enrollments")
@RequiredArgsConstructor
public class EnrollmentController {

    private final EnrollmentService service;

    @Operation(summary = "Enroll a student in a course")
    @PostMapping
    public ResponseEntity<Enrollment> enroll(@RequestBody @Valid EnrollmentRequest request,
                                             Authentication authentication) {
        log.info("=== Enrollment Request Started ===");
        log.info("Request body - courseId: {}", request.getCourseId());
        log.info("Authentication - user: {}, authorities: {}",
                authentication.getName(),
                authentication.getAuthorities());

        String userId = authentication.getName();
        Enrollment enrollment = service.enroll(userId, request.getCourseId());

        log.info("Enrollment created successfully - enrollmentId: {}, userId: {}, courseId: {}",
                enrollment.getEnrollmentId(), enrollment.getUserId(), enrollment.getCourseId());
        log.info("=== Enrollment Request Completed ===");

        return ResponseEntity.ok(enrollment);
    }


    @Operation(summary = "Get all enrollments of the logged-in user")
    @GetMapping("/me")
    public ResponseEntity<List<Enrollment>> myEnrollments(Authentication authentication) {
        log.info("Fetching enrollments for user: {}", authentication.getName());
        String userId = authentication.getName();
        List<Enrollment> enrollments = service.getMyEnrollments(userId);
        log.info("Found {} enrollments for user: {}", enrollments.size(), userId);
        return ResponseEntity.ok(enrollments);
    }


    @Operation(summary = "Get a specific enrollment by ID")
    @GetMapping("/{enrollmentId}")
    public ResponseEntity<Enrollment> getEnrollment(@PathVariable Long enrollmentId,
                                                    Authentication authentication) {
        log.info("Fetching enrollment: {}", enrollmentId);
        Enrollment e = service.getEnrollment(enrollmentId);
        String currentUser = authentication.getName();

        if (!e.getUserId().equals(currentUser) && !hasRole(authentication, "ADMIN")) {
            log.warn("Access denied - user: {} attempted to access enrollment: {} owned by: {}",
                    currentUser, enrollmentId, e.getUserId());
            return ResponseEntity.status(403).build();
        }
        return ResponseEntity.ok(e);
    }


    @Operation(summary = "Mark a lesson as complete")
    @PostMapping("/{enrollmentId}/lessons/{lessonId}/complete")
    public ResponseEntity<Progress> markLessonComplete(@PathVariable Long enrollmentId,
                                                       @PathVariable Long lessonId,
                                                       Authentication authentication) {
        log.info("Marking lesson complete - enrollmentId: {}, lessonId: {}, user: {}",
                enrollmentId, lessonId, authentication.getName());
        String userId = authentication.getName();
        String role = getRole(authentication);
        Progress progress = service.markLessonComplete(enrollmentId, lessonId, userId, role);
        log.info("Lesson marked complete - progressId: {}", progress.getProgressId());
        return ResponseEntity.ok(progress);
    }

    /**
     * Generate a course completion certificate
     */
    @Operation(summary = "Generate a certificate for a completed course")
    @PostMapping("/{enrollmentId}/certificate")
    public ResponseEntity<Certificate> generateCertificate(@PathVariable Long enrollmentId,
                                                           Authentication authentication) {
        log.info("Generating certificate - enrollmentId: {}, user: {}",
                enrollmentId, authentication.getName());
        String userId = authentication.getName();
        String role = getRole(authentication);
        Certificate certificate = service.generateCertificate(enrollmentId, userId, role);
        log.info("Certificate generated - certificateId: {}", certificate.getCertificateId());
        return ResponseEntity.ok(certificate);
    }


    private boolean hasRole(Authentication auth, String role) {
        return auth.getAuthorities()
                .stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(a -> a.equals("ROLE_" + role));
    }

    private String getRole(Authentication auth) {
        return auth.getAuthorities()
                .stream()
                .filter(a -> a.getAuthority().startsWith("ROLE_"))
                .findFirst()
                .map(GrantedAuthority::getAuthority)
                .map(s -> s.replace("ROLE_", ""))
                .orElse("USER");
    }
}