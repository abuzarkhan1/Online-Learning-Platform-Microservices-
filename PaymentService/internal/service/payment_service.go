package service

import (
	"context"
	"errors"
	"time"

	"github.com/google/uuid"
	stripe "github.com/stripe/stripe-go/v79"
	"github.com/stripe/stripe-go/v79/paymentintent"

	"paymentservice/internal/config"
	"paymentservice/internal/domain"
	"paymentservice/internal/repository"
)

type PaymentService interface {
	CreatePayment(ctx context.Context, userID, enrollmentID string, amountCents int64, currency string, description string, paymentMethodID *string) (*domain.Payment, error)
	GetPayment(ctx context.Context, id string) (*domain.Payment, error)
	ListByUser(ctx context.Context, userID string, limit, offset int) ([]domain.Payment, error)
	ListByEnrollment(ctx context.Context, enrollmentID string, limit, offset int) ([]domain.Payment, error)
}

type paymentService struct {
	cfg  config.Config
	repo repository.PaymentRepository
}

func NewPaymentService(cfg config.Config, repo repository.PaymentRepository) PaymentService {
	stripe.Key = cfg.StripeSecretKey
	return &paymentService{cfg: cfg, repo: repo}
}

func (s *paymentService) CreatePayment(ctx context.Context, userID, enrollmentID string, amountCents int64, currency string, description string, paymentMethodID *string) (*domain.Payment, error) {
	if amountCents <= 0 {
		return nil, errors.New("amount must be positive")
	}
	if enrollmentID == "" {
		return nil, errors.New("enrollmentId is required")
	}
	params := &stripe.PaymentIntentParams{
		Amount:      stripe.Int64(amountCents),
		Currency:    stripe.String(currency),
		Description: stripe.String(description),
		Confirm:     stripe.Bool(true),
		AutomaticPaymentMethods: &stripe.PaymentIntentAutomaticPaymentMethodsParams{
			Enabled:        stripe.Bool(true),
			AllowRedirects: stripe.String(string(stripe.PaymentIntentAutomaticPaymentMethodsAllowRedirectsNever)),
		},
	}
	if paymentMethodID != nil && *paymentMethodID != "" {
		params.PaymentMethod = stripe.String(*paymentMethodID)
	}
	pi, err := paymentintent.New(params)
	if err != nil {
		return nil, err
	}
	now := time.Now().UTC()
	providerRef := pi.ID
	p := domain.Payment{
		ID:           uuid.NewString(),
		UserID:       userID,
		EnrollmentID: enrollmentID,
		AmountCents:  amountCents,
		Currency:     currency,
		Status:       domain.PaymentStatusSucceeded,
		Provider:     "stripe",
		ProviderRef:  &providerRef,
		CreatedAt:    now,
	}
	if err := s.repo.Create(ctx, p); err != nil {
		return nil, err
	}
	// fire and forget enrollment callback
	go notifyEnrollmentPaid(s.cfg, p)
	return &p, nil
}

func (s *paymentService) GetPayment(ctx context.Context, id string) (*domain.Payment, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *paymentService) ListByUser(ctx context.Context, userID string, limit, offset int) ([]domain.Payment, error) {
	return s.repo.ListByUser(ctx, userID, limit, offset)
}

func (s *paymentService) ListByEnrollment(ctx context.Context, enrollmentID string, limit, offset int) ([]domain.Payment, error) {
	return s.repo.ListByEnrollment(ctx, enrollmentID, limit, offset)
}
