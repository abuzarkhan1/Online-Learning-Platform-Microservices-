package com.abuzar.enrollmentservice.repository;

import com.abuzar.enrollmentservice.models.Enrollment;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface EnrollmentRepository extends JpaRepository<Enrollment, Long> {
    List<Enrollment> findByUserId(String userId);
    List<Enrollment> findByUserIdAndCourseId(String userId, Long courseId);
}