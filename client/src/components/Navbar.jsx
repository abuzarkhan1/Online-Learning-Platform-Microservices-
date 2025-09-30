import { Link, useNavigate } from 'react-router-dom'
import { getToken, clearToken } from '../lib/auth'

export default function Navbar({ theme, setTheme }){
  const nav = useNavigate()
  const authed = !!getToken()
  const toggle = ()=> setTheme(theme === 'dark' ? 'light' : 'dark')
  return (
    <header className="border-b border-gray-200 dark:border-gray-800">
      <div className="max-w-6xl mx-auto p-4 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link to="/" className="font-semibold">Project</Link>
          <Link to="/courses" className="text-sm hover:underline">Courses</Link>
          {authed && <>
            <Link to="/me/enrollments" className="text-sm hover:underline">My Enrollments</Link>
            <Link to="/me/payments" className="text-sm hover:underline">My Payments</Link>
          </>}
        </div>
        <div className="flex items-center gap-3">
          <button onClick={toggle} className="px-3 py-1 rounded bg-gray-100 dark:bg-gray-800">
            {theme === 'dark' ? 'Light' : 'Dark'}
          </button>
          {authed ? (
            <button onClick={()=>{clearToken(); nav('/login')}} className="px-3 py-1 rounded bg-red-600 text-white">Logout</button>
          ) : (
            <>
              <Link to="/login" className="px-3 py-1 rounded bg-blue-600 text-white">Login</Link>
              <Link to="/register" className="px-3 py-1 rounded border">Register</Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
