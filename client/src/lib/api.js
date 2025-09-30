import axios from 'axios'

const create = (baseURL) => {
  const client = axios.create({ baseURL })
  client.interceptors.request.use(cfg => {
    const token = localStorage.getItem('token')
    if (token) cfg.headers.Authorization = `Bearer ${token}`
    return cfg
  })
  return client
}

export const userApi = create(import.meta.env.VITE_USER_API || 'http://localhost:3000/api/users')
export const courseApi = create(import.meta.env.VITE_COURSE_API || 'http://localhost:3002')
export const enrollApi = create(import.meta.env.VITE_ENROLL_API || 'http://localhost:3003')
export const paymentApi = create(import.meta.env.VITE_PAYMENT_API || 'http://localhost:3004')
