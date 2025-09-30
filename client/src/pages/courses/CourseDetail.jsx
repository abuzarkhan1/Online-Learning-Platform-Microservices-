import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { courseApi, enrollApi } from '../../lib/api'

export default function CourseDetail(){
  const { id } = useParams()
  const nav = useNavigate()
  const [course,setCourse]=useState(null)
  useEffect(()=>{ (async()=>{
    const { data } = await courseApi.get(`/courses/${id}`)
    setCourse(data)
  })() },[id])
  if(!course) return <p>Loading...</p>
  const buy = async () => {
    try {
      const { data } = await enrollApi.post('/enrollments', { courseId: Number(id) })
      const enrollmentId = data?.enrollmentId ?? data?.id ?? data
      const amountCents = typeof course?.priceCents === 'number' ? course.priceCents : Math.round(Number(course?.price || 0) * 100)
      if (enrollmentId) {
        nav(`/checkout/${enrollmentId}`, { state: { amountCents, currency: 'usd' } })
      } else {
        alert('Failed to create enrollment')
      }
    } catch (e) {
      alert(e?.response?.data?.error || 'Failed to create enrollment')
    }
  }
  return (
    <div className="mt-6">
      <h1 className="text-2xl font-semibold">{course.title}</h1>
      <p className="opacity-80 mt-2">{course.description}</p>
      <div className="mt-4 flex items-center gap-3">
        <span className="font-semibold text-lg">${typeof course?.priceCents === 'number' ? (course.priceCents/100).toFixed(2) : String(course?.price)}</span>
        <button onClick={buy} className="px-4 py-2 rounded bg-green-600 text-white">Buy</button>
      </div>
    </div>
  )
}
