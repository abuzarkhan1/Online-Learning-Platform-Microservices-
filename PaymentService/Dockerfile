FROM golang:1.21-alpine AS build
WORKDIR /app
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o paymentservice ./cmd/server

FROM gcr.io/distroless/base-debian12
WORKDIR /
COPY --from=build /app/paymentservice /paymentservice
ENV PORT=3004
EXPOSE 3004
USER nonroot:nonroot
ENTRYPOINT ["/paymentservice"]


