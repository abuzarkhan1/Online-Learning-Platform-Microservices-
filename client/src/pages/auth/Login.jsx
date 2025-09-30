import { useState } from 'react'
import { userApi } from '../../lib/api'
import { setToken } from '../../lib/auth'
import { useNavigate, Link } from 'react-router-dom'

export default function Login(){
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [err,setErr]=useState('')
  const nav = useNavigate()
  const submit = async (e)=>{
    e.preventDefault(); setErr('')
    try{
      const { data } = await userApi.post('/login',{ email, password })
      setToken(data.token)
      nav('/courses')
      
    }catch(e){ setErr(e?.response?.data?.error || 'Login failed') }
  }
  return (
    <div className="max-w-md mx-auto mt-10">
      <h1 className="text-2xl mb-4">Login</h1>
      <form onSubmit={submit} className="space-y-3">
        <input className="w-full border rounded px-3 py-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" type="password" placeholder="Password" value={password} onChange={e=>setPassword(e.target.value)} />
        {err && <p className="text-red-600 text-sm">{err}</p>}
        <button className="w-full bg-blue-600 text-white py-2 rounded">Login</button>
      </form>
      <p className="text-sm mt-3">No account? <Link to="/register" className="underline">Register</Link></p>
    </div>
  )
}
