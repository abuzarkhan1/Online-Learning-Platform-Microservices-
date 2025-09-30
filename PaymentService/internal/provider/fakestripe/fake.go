package fakestripe

import (
	"context"
	"fmt"
	"math/rand"
	"time"
)

type Client struct{}

func New() *Client { return &Client{} }

type ChargeRequest struct {
	AmountCents int64
	Currency    string
	Description string
}

type ChargeResponse struct {
	ID     string
	Status string
}

func (c *Client) Charge(ctx context.Context, req ChargeRequest) (*ChargeResponse, error) {
	_ = ctx
	time.Sleep(100 * time.Millisecond)
	id := fmt.Sprintf("fake_%d", rand.New(rand.NewSource(time.Now().UnixNano())).Int63())
	return &ChargeResponse{ID: id, Status: "succeeded"}, nil
}
