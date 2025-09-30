package com.abuzar.enrollmentservice.models;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "certificates")
@Data
@NoArgsConstructor
public class Certificate {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long certificateId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "enrollment_id")
    @JsonBackReference          // ✅ prevent recursion
    private Enrollment enrollment;

    private LocalDateTime issuedAt = LocalDateTime.now();
    private String url;
}
