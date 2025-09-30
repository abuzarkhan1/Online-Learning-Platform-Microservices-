package repository

import (
	"context"
	"time"

	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgxpool"

	"paymentservice/internal/domain"
)

type PaymentRepository interface {
	Create(ctx context.Context, p domain.Payment) error
	GetByID(ctx context.Context, id string) (*domain.Payment, error)
	ListByUser(ctx context.Context, userID string, limit, offset int) ([]domain.Payment, error)
	ListByEnrollment(ctx context.Context, enrollmentID string, limit, offset int) ([]domain.Payment, error)
}

type pgRepo struct {
	pool *pgxpool.Pool
}

func NewPostgres(pool *pgxpool.Pool) PaymentRepository {
	return &pgRepo{pool: pool}
}

func (r *pgRepo) Create(ctx context.Context, p domain.Payment) error {
	_, err := r.pool.Exec(ctx, `
INSERT INTO payments (id, user_id, enrollment_id, amount_cents, currency, status, provider, provider_ref, created_at)
VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
`, p.ID, p.UserID, p.EnrollmentID, p.AmountCents, p.Currency, p.Status, p.Provider, p.ProviderRef, p.CreatedAt)
	return err
}

func scanPayment(row pgx.Row) (*domain.Payment, error) {
	var (
		p           domain.Payment
		providerRef *string
		createdAt   time.Time
	)
	if err := row.Scan(&p.ID, &p.UserID, &p.EnrollmentID, &p.AmountCents, &p.Currency, &p.Status, &p.Provider, &providerRef, &createdAt); err != nil {
		return nil, err
	}
	p.ProviderRef = providerRef
	p.CreatedAt = createdAt
	return &p, nil
}

func (r *pgRepo) GetByID(ctx context.Context, id string) (*domain.Payment, error) {
	row := r.pool.QueryRow(ctx, `
SELECT id, user_id, enrollment_id, amount_cents, currency, status, provider, provider_ref, created_at
FROM payments WHERE id=$1
`, id)
	return scanPayment(row)
}

func (r *pgRepo) ListByUser(ctx context.Context, userID string, limit, offset int) ([]domain.Payment, error) {
	rows, err := r.pool.Query(ctx, `
SELECT id, user_id, enrollment_id, amount_cents, currency, status, provider, provider_ref, created_at
FROM payments WHERE user_id=$1 ORDER BY created_at DESC LIMIT $2 OFFSET $3
`, userID, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []domain.Payment
	for rows.Next() {
		p, err := scanPayment(rows)
		if err != nil {
			return nil, err
		}
		out = append(out, *p)
	}
	return out, rows.Err()
}

func (r *pgRepo) ListByEnrollment(ctx context.Context, enrollmentID string, limit, offset int) ([]domain.Payment, error) {
	rows, err := r.pool.Query(ctx, `
SELECT id, user_id, enrollment_id, amount_cents, currency, status, provider, provider_ref, created_at
FROM payments WHERE enrollment_id=$1 ORDER BY created_at DESC LIMIT $2 OFFSET $3
`, enrollmentID, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []domain.Payment
	for rows.Next() {
		p, err := scanPayment(rows)
		if err != nil {
			return nil, err
		}
		out = append(out, *p)
	}
	return out, rows.Err()
}
