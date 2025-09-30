import { useState } from 'react'
import { userApi } from '../../lib/api'
import { useNavigate, Link } from 'react-router-dom'

export default function Register(){
  const [name,setName]=useState('')
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [err,setErr]=useState('')
  const nav=useNavigate()
  const submit = async (e)=>{
    e.preventDefault(); setErr('')
    try{
      await userApi.post('/auth/register',{ name,email,password })
      nav('/login')
    }catch(e){ setErr(e?.response?.data?.error || 'Register failed') }
  }
  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl mb-4">Register</h1>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full border rounded px-3 py-2" placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        {err && <p className="text-red-600 text-sm">{err}</p>}
        <button className="w-full bg-blue-600 text-white py-2 rounded">Create Account</button>
      </form>
      <p className="text-sm mt-3">Have an account? <Link to="/login" className="underline">Login</Link></p>
    </div>
  )
}
