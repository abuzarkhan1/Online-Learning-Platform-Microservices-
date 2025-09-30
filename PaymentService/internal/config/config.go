package config

import (
	"os"
)

type Config struct {
	Port                 string
	DatabaseURL          string
	EnrollmentServiceURL string
	ServiceName          string
	StripePublishableKey string
	StripeSecretKey      string
	JWTSecret            string
	FrontendOrigin       string
}

func Load() Config {
	cfg := Config{
		Port:                 getenv("PORT", "3004"),
		DatabaseURL:          getenv("DATABASE_URL", "postgres://postgres:root@localhost:5432/paymentdb?sslmode=disable"),
		EnrollmentServiceURL: getenv("ENROLLMENT_SERVICE_URL", "http://localhost:3003"),
		ServiceName:          getenv("SERVICE_NAME", "payment-service"),
		StripePublishableKey: getenv("", ""),
		StripeSecretKey:      getenv("", ""),
		JWTSecret:            getenv("JWT_SECRET", "JWT_SECRETJWT_SECRETJWT_SECRETJWT_SECRETJWT_SECRET"),
		FrontendOrigin:       getenv("FRONTEND_ORIGIN", "http://localhost:5173"),
	}
	return cfg
}

func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}
