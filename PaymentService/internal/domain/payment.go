package domain

import "time"

type PaymentStatus string

const (
	PaymentStatusPending   PaymentStatus = "pending"
	PaymentStatusSucceeded PaymentStatus = "succeeded"
	PaymentStatusFailed    PaymentStatus = "failed"
)

type Payment struct {
	ID           string        `json:"id"`
	UserID       string        `json:"userId"`
	EnrollmentID string        `json:"enrollmentId"`
	AmountCents  int64         `json:"amountCents"`
	Currency     string        `json:"currency"`
	Status       PaymentStatus `json:"status"`
	Provider     string        `json:"provider"`
	ProviderRef  *string       `json:"providerRef,omitempty"`
	CreatedAt    time.Time     `json:"createdAt"`
}
