## PaymentService (Go + Gin)

Features:
- Fake Stripe charges
- Store payment history in Postgres
- Notify EnrollmentService on success

### Run locally (port 3004)
1. Set env vars or copy `.env.example` to `.env` and edit values.
2. Ensure Postgres is running and `DATABASE_URL` is valid.
3. Install deps and run:

```bash
go mod tidy
PORT=3004 ENROLLMENT_SERVICE_URL=http://localhost:3003 go run ./cmd/server
```

### API
- POST `/api/payments/` { userId, enrollmentId, amountCents, currency, description }
- GET `/api/payments/:id`
- GET `/api/payments/user/:userId?limit=&offset=`
- GET `/api/payments/enrollment/:enrollmentId?limit=&offset=`

### Docker
```bash
docker build -t paymentservice .
docker run -e DATABASE_URL=... -e ENROLLMENT_SERVICE_URL=... -e JWT_SECRET=... -e STRIPE_SECRET_KEY=... -p 3004:3004 paymentservice
```


