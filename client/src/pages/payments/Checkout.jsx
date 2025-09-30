import { CardElement, useStripe, useElements } from "@stripe/react-stripe-js";
import { useParams, useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";
import { paymentApi } from "../../lib/api";

export default function Checkout() {
  const { enrollmentId } = useParams();
  const location = useLocation();
  const amountFromState = location.state?.amount || location.state?.amountCents || 0;
  const currencyFromState = location.state?.currency || "usd";
  const stripe = useStripe();
  const elements = useElements();
  const nav = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const amountCents = Math.round(amountFromState * 100);
  const displayAmount = (amountCents / 100).toFixed(2);

  const pay = async () => {
    if (!stripe || !elements) return;
    setLoading(true);
    setError("");
    try {
      const { paymentMethod, error: pmErr } = await stripe.createPaymentMethod({
        type: "card",
        card: elements.getElement(CardElement),
      });
      if (pmErr) throw pmErr;
      
      const body = {
        enrollmentId: String(enrollmentId),
        amountCents: amountCents,
        currency: currencyFromState,
        description: "Course purchase",
        paymentMethodId: paymentMethod.id,
      };
      
      await paymentApi.post("/api/payments/", body);
      nav("/me/payments");
    } catch (e) {
      setError(e?.message || e?.response?.data?.error || "Payment failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-8">
      <h1 className="text-2xl mb-4">Checkout</h1>
      <p className="mb-4 text-lg">
        Total: <span className="font-bold">${displayAmount} {currencyFromState.toUpperCase()}</span>
      </p>
      <div className="border rounded p-4 bg-gray-50 dark:bg-gray-900">
        <CardElement />
      </div>
      {error && <p className="text-red-600 text-sm mt-2">{error}</p>}
      <button
        disabled={loading || !stripe}
        onClick={pay}
        className="mt-4 w-full bg-blue-600 text-white py-2 rounded disabled:opacity-50"
      >
        {loading ? "Processing..." : `Pay $${displayAmount}`}
      </button>
    </div>
  );
}