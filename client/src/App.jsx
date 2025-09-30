import { Routes, Route, Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Navbar from './components/Navbar'
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import Courses from './pages/courses/Courses'
import CourseDetail from './pages/courses/CourseDetail'
import Checkout from './pages/payments/Checkout'
import MyEnrollments from './pages/enrollments/MyEnrollments'
import MyPayments from './pages/payments/MyPayments'
import { getToken } from './lib/auth'

function RequireAuth({ children }){
  return getToken() ? children : <Navigate to="/login" replace />
}

export default function App(){
  const [theme, setTheme] = useState(()=> localStorage.getItem('theme') || 'light')
  useEffect(()=>{
    document.documentElement.classList.toggle('dark', theme === 'dark')
    localStorage.setItem('theme', theme)
  },[theme])
  return (
    <div className="min-h-screen bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-100">
      <Navbar theme={theme} setTheme={setTheme} />
      <div className="max-w-6xl mx-auto p-4">
        <Routes>
          <Route path="/" element={<Navigate to="/courses" replace />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/courses" element={<Courses />} />
          <Route path="/courses/:id" element={<CourseDetail />} />
          <Route path="/checkout/:enrollmentId" element={<RequireAuth><Checkout /></RequireAuth>} />
          <Route path="/me/enrollments" element={<RequireAuth><MyEnrollments /></RequireAuth>} />
          <Route path="/me/payments" element={<RequireAuth><MyPayments /></RequireAuth>} />
        </Routes>
      </div>
    </div>
  )
}
