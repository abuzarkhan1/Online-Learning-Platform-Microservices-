package router

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"

	"paymentservice/internal/config"
	"paymentservice/internal/http/middleware"
	"paymentservice/internal/repository"
	"paymentservice/internal/service"
)

type createPaymentRequest struct {
	EnrollmentID    string `json:"enrollmentId" binding:"required"`
	AmountCents     int64  `json:"amountCents" binding:"required,gt=0"`
	Currency        string `json:"currency" binding:"required"`
	Description     string `json:"description"`
	PaymentMethodID string `json:"paymentMethodId"`
}

func Register(r *gin.Engine, cfg config.Config, pool *pgxpool.Pool) {
	repo := repository.NewPostgres(pool)
	svc := service.NewPaymentService(cfg, repo)

	auth := middleware.AuthMiddleware(middleware.JWTConfig{Secret: cfg.JWTSecret, AuthHeader: "Authorization", UserIDClaim: "id"})
	api := r.Group("/api/payments", auth)
	{
		api.POST("/", func(c *gin.Context) {
			var req createPaymentRequest
			if err := c.ShouldBindJSON(&req); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			userID := c.GetString("userId")
			var pmIDPtr *string
			if req.PaymentMethodID != "" {
				pmIDPtr = &req.PaymentMethodID
			}
			p, err := svc.CreatePayment(c.Request.Context(), userID, req.EnrollmentID, req.AmountCents, req.Currency, req.Description, pmIDPtr)
			if err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}
			c.JSON(http.StatusCreated, p)
		})

		api.GET("/:id", func(c *gin.Context) {
			id := c.Param("id")
			p, err := svc.GetPayment(c.Request.Context(), id)
			if err != nil {
				c.JSON(http.StatusNotFound, gin.H{"error": "not found"})
				return
			}
			c.JSON(http.StatusOK, p)
		})

		api.GET("/user/me", func(c *gin.Context) {
			userID := c.GetString("userId")
			limit := parseInt(c.Query("limit"), 20)
			offset := parseInt(c.Query("offset"), 0)
			list, err := svc.ListByUser(c.Request.Context(), userID, limit, offset)
			if err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			c.JSON(http.StatusOK, list)
		})

		api.GET("/enrollment/:enrollmentId", func(c *gin.Context) {
			enrollmentID := c.Param("enrollmentId")
			limit := parseInt(c.Query("limit"), 20)
			offset := parseInt(c.Query("offset"), 0)
			list, err := svc.ListByEnrollment(c.Request.Context(), enrollmentID, limit, offset)
			if err != nil {
				c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
				return
			}
			c.JSON(http.StatusOK, list)
		})
	}
}

func parseInt(s string, def int) int {
	if s == "" {
		return def
	}
	if v, err := strconv.Atoi(s); err == nil {
		return v
	}
	return def
}
