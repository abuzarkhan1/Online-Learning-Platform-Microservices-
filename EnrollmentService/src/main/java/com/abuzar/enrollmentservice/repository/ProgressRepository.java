package com.abuzar.enrollmentservice.repository;

import com.abuzar.enrollmentservice.models.Progress;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface ProgressRepository extends JpaRepository<Progress, Long> {
    List<Progress> findByEnrollmentEnrollmentId(Long enrollmentId);

    // Method to find progress by enrollment ID and lesson ID
    Optional<Progress> findByEnrollment_EnrollmentIdAndLessonId(Long enrollmentId, Long lessonId);
}