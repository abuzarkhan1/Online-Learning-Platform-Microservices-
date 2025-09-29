package com.abuzar.enrollmentservice.models;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Table(name = "progress")
@Data
@NoArgsConstructor
public class Progress {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long progressId;

    // Child side → don't serialize back to avoid loop
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "enrollment_id")
    @JsonBackReference           // ✅ avoids infinite recursion
    private Enrollment enrollment;

    private Long lessonId;
    private boolean completed = false;
    private LocalDateTime completedAt;
}
