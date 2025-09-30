package com.abuzar.enrollmentservice.models;

import com.fasterxml.jackson.annotation.JsonManagedReference;
import jakarta.persistence.*;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "enrollments")
@Data
@NoArgsConstructor
public class Enrollment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long enrollmentId;

    @Column(nullable = false)
    private String userId;

    @Column(nullable = false)
    private Long courseId;

    @Column(nullable = false)
    private LocalDateTime enrolledAt = LocalDateTime.now();

    @Enumerated(EnumType.STRING)
    private Status status = Status.IN_PROGRESS;

    public enum Status {
        IN_PROGRESS, COMPLETED, CANCELLED
    }

    // Parent side of the relationship → serialize this
    @OneToMany(mappedBy = "enrollment", cascade = CascadeType.ALL, orphanRemoval = true)
    @JsonManagedReference        // ✅ avoids infinite recursion
    private List<Progress> progressList;
}
