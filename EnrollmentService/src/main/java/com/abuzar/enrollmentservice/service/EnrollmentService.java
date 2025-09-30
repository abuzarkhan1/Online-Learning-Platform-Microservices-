package com.abuzar.enrollmentservice.service;

import com.abuzar.enrollmentservice.models.Certificate;
import com.abuzar.enrollmentservice.models.Enrollment;
import com.abuzar.enrollmentservice.models.Progress;
import com.abuzar.enrollmentservice.repository.CertificateRepository;
import com.abuzar.enrollmentservice.repository.EnrollmentRepository;
import com.abuzar.enrollmentservice.repository.ProgressRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.time.LocalDateTime;
import java.util.List;

@Slf4j
@Service
@RequiredArgsConstructor
public class EnrollmentService {

    private final EnrollmentRepository enrollmentRepo;
    private final ProgressRepository progressRepo;
    private final CertificateRepository certificateRepo;

    @Transactional
    public Enrollment enroll(String userId, Long courseId) {
        log.info("Enrolling user {} in course {}", userId, courseId);

        // Check if already enrolled
        List<Enrollment> existing = enrollmentRepo.findByUserIdAndCourseId(userId, courseId);
        if (!existing.isEmpty()) {
            log.warn("User {} is already enrolled in course {}", userId, courseId);
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "You are already enrolled in this course");
        }

        Enrollment e = new Enrollment();
        e.setUserId(userId);
        e.setCourseId(courseId);
        e.setEnrolledAt(LocalDateTime.now());
        e.setStatus(Enrollment.Status.IN_PROGRESS);

        Enrollment saved = enrollmentRepo.save(e);
        log.info("Enrollment created: id={}", saved.getEnrollmentId());
        return saved;
    }

    public List<Enrollment> getMyEnrollments(String userId) {
        log.debug("Fetching enrollments for user: {}", userId);
        return enrollmentRepo.findByUserId(userId);
    }

    public Enrollment getEnrollment(Long enrollmentId) {
        log.debug("Fetching enrollment: {}", enrollmentId);
        return enrollmentRepo.findById(enrollmentId)
                .orElseThrow(() -> {
                    log.error("Enrollment not found: {}", enrollmentId);
                    return new ResponseStatusException(HttpStatus.NOT_FOUND, "Enrollment not found");
                });
    }

    @Transactional
    public Progress markLessonComplete(Long enrollmentId, Long lessonId,
                                       String currentUserId, String currentUserRole) {
        log.info("Marking lesson complete - enrollmentId: {}, lessonId: {}, user: {}",
                enrollmentId, lessonId, currentUserId);

        Enrollment enrollment = getEnrollment(enrollmentId);

        if (!enrollment.getUserId().equals(currentUserId) &&
                !("ADMIN".equalsIgnoreCase(currentUserRole))) {
            log.warn("User {} not authorized to mark lesson complete for enrollment {}",
                    currentUserId, enrollmentId);
            throw new ResponseStatusException(HttpStatus.FORBIDDEN,
                    "You are not authorized to complete lessons for this enrollment");
        }

        // Check if progress already exists
        Progress p = progressRepo.findByEnrollment_EnrollmentIdAndLessonId(enrollmentId, lessonId)
                .orElse(new Progress());

        if (p.getProgressId() != null && p.isCompleted()) {
            log.info("Lesson {} already completed for enrollment {}", lessonId, enrollmentId);
            return p;
        }

        p.setEnrollment(enrollment);
        p.setLessonId(lessonId);
        p.setCompleted(true);
        p.setCompletedAt(LocalDateTime.now());

        Progress saved = progressRepo.save(p);
        log.info("Progress saved: id={}", saved.getProgressId());
        return saved;
    }

    @Transactional
    public Certificate generateCertificate(Long enrollmentId,
                                           String currentUserId,
                                           String currentUserRole) {
        log.info("Generating certificate for enrollment: {}, user: {}",
                enrollmentId, currentUserId);

        Enrollment enrollment = getEnrollment(enrollmentId);

        // Only owner or admin
        if (!enrollment.getUserId().equals(currentUserId) &&
                !("ADMIN".equalsIgnoreCase(currentUserRole))) {
            log.warn("User {} not authorized to generate certificate for enrollment {}",
                    currentUserId, enrollmentId);
            throw new ResponseStatusException(HttpStatus.FORBIDDEN,
                    "You are not authorized to generate a certificate for this enrollment");
        }

        // Check if certificate already exists
        Certificate existingCert = certificateRepo.findByEnrollmentEnrollmentId(enrollmentId);
        if (existingCert != null) {
            log.info("Certificate already exists for enrollment {}: certificateId={}",
                    enrollmentId, existingCert.getCertificateId());
            return existingCert;
        }

        enrollment.setStatus(Enrollment.Status.COMPLETED);
        enrollmentRepo.save(enrollment);

        Certificate cert = new Certificate();
        cert.setEnrollment(enrollment);
        cert.setIssuedAt(LocalDateTime.now());
        cert.setUrl("https://example.com/certs/" + enrollmentId + ".pdf");

        Certificate saved = certificateRepo.save(cert);
        log.info("Certificate generated: id={}", saved.getCertificateId());
        return saved;
    }
}