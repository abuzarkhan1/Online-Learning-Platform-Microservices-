import { useEffect, useState } from 'react'
import { courseApi } from '../../lib/api'
import { Link } from 'react-router-dom'

export default function Courses() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  useEffect(() => {
    (async () => {
      try {
        const { data } = await courseApi.get('/courses'); setItems(data || [])
        console.log(data)
      }

      finally { setLoading(false) }
    })()
  }, [])
  if (loading) return <p>Loading...</p>
  return (
    <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-6">
      {items.map(c => (
        <div key={c.id} className="border rounded p-4 bg-gray-50 dark:bg-gray-900">
          <h3 className="font-semibold mb-1">{c.title}</h3>
          <p className="text-sm opacity-80 line-clamp-3">{c.description}</p>
          <div className="flex items-center justify-between mt-3">
            <span className="font-semibold">${c.price}</span>
            <Link to={`/courses/${c.id}`} className="px-3 py-1 rounded bg-blue-600 text-white">View</Link>
          </div>
        </div>
      ))}
    </div>
  )
}
