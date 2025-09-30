import { useEffect, useState } from 'react'
import { paymentApi } from '../../lib/api'

export default function MyPayments(){
  const [items,setItems]=useState([])
  useEffect(()=>{ (async()=>{
    const { data } = await paymentApi.get('/api/payments/user/me?limit=50')
    setItems(data||[])
  })() },[])
  return (
    <div className="mt-6 space-y-3">
      <h1 className="text-2xl font-semibold">My Payments</h1>
      {items.map(p=> (
        <div key={p.id} className="border rounded p-3 bg-gray-50 dark:bg-gray-900">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold">{p.provider} — {(p.amountCents/100).toFixed(2)} {String(p.currency).toUpperCase()}</p>
              <p className="text-sm opacity-80">Status: {p.status} | Ref: {p.providerRef}</p>
            </div>
            <span className="text-xs opacity-70">{new Date(p.createdAt).toLocaleString()}</span>
          </div>
        </div>
      ))}
    </div>
  )
}
