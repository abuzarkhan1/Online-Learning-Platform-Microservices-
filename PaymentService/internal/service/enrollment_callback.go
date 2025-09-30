package service

import (
	"bytes"
	"encoding/json"
	"log"
	"net/http"
	"time"

	"paymentservice/internal/config"
	"paymentservice/internal/domain"
)

type enrollmentPaidPayload struct {
	PaymentID    string `json:"paymentId"`
	EnrollmentID string `json:"enrollmentId"`
	UserID       string `json:"userId"`
	AmountCents  int64  `json:"amountCents"`
	Currency     string `json:"currency"`
	Status       string `json:"status"`
}

func notifyEnrollmentPaid(cfg config.Config, p domain.Payment) {
	payload := enrollmentPaidPayload{
		PaymentID:    p.ID,
		EnrollmentID: p.EnrollmentID,
		UserID:       p.UserID,
		AmountCents:  p.AmountCents,
		Currency:     p.Currency,
		Status:       string(p.Status),
	}
	b, _ := json.Marshal(payload)
	client := &http.Client{Timeout: 5 * time.Second}
	url := cfg.EnrollmentServiceURL + "/internal/enrollments/mark-paid"
	req, err := http.NewRequest(http.MethodPost, url, bytes.NewReader(b))
	if err != nil {
		log.Printf("enrollment notify build req error: %v", err)
		return
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := client.Do(req)
	if err != nil {
		log.Printf("enrollment notify request error: %v", err)
		return
	}
	defer resp.Body.Close()
	if resp.StatusCode >= 300 {
		log.Printf("enrollment notify non-2xx: %d", resp.StatusCode)
	}
}
