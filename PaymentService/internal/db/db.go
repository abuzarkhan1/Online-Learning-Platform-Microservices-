package db

import (
	"context"

	"github.com/jackc/pgx/v5/pgxpool"
)

func Connect(ctx context.Context, databaseURL string) (*pgxpool.Pool, error) {
	cfg, err := pgxpool.ParseConfig(databaseURL)
	if err != nil {
		return nil, err
	}
	pool, err := pgxpool.NewWithConfig(ctx, cfg)
	if err != nil {
		return nil, err
	}
	if err := pool.Ping(ctx); err != nil {
		return nil, err
	}
	return pool, nil
}

// internal/db/db.go
func AutoMigrate(ctx context.Context, pool *pgxpool.Pool) error {
	_, err := pool.Exec(ctx, `
CREATE TABLE IF NOT EXISTS payments (
    id UUID PRIMARY KEY,
    user_id TEXT NOT NULL,
    enrollment_id TEXT NOT NULL,  -- Already TEXT, good!
    amount_cents BIGINT NOT NULL,
    currency TEXT NOT NULL,
    status TEXT NOT NULL,
    provider TEXT NOT NULL,
    provider_ref TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id);
CREATE INDEX IF NOT EXISTS idx_payments_enrollment_id ON payments(enrollment_id);
`)
	return err
}
