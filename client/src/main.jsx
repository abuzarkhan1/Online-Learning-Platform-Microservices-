import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Elements } from '@stripe/react-stripe-js'
import { loadStripe } from '@stripe/stripe-js'
import './index.css'
import App from './App.jsx'

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PK || '')

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Elements stripe={stripePromise}>
        <App />
      </Elements>
    </BrowserRouter>
  </StrictMode>,
)
