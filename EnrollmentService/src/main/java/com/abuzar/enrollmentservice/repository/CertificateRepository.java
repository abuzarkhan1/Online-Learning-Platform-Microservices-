package com.abuzar.enrollmentservice.repository;

import com.abuzar.enrollmentservice.models.Certificate;
import org.springframework.data.jpa.repository.JpaRepository;

public interface CertificateRepository extends JpaRepository<Certificate, Long> {
    Certificate findByEnrollmentEnrollmentId(Long enrollmentId);
}