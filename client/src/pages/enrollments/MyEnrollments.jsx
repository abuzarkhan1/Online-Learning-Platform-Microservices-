import { useEffect, useState } from 'react'
import { enrollApi } from '../../lib/api'

export default function MyEnrollments(){
  const [items,setItems]=useState([])
  useEffect(()=>{ (async()=>{
    const { data } = await enrollApi.get('/enrollments/me')
    setItems(data||[])
  })() },[])
  return (
    <div className="mt-6 space-y-3">
      <h1 className="text-2xl font-semibold">My Enrollments</h1>
      {items.map(e=> (
        <div key={e.enrollmentId} className="border rounded p-3 bg-gray-50 dark:bg-gray-900">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-semibold">Enrollment #{e.enrollmentId}</p>
              <p className="text-sm opacity-80">Status: {e.status}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
