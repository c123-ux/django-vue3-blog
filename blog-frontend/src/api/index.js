import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

api.interceptors.response.use(
  response => response,
  error => {
    if (!error.config) {
      return Promise.reject(error)
    }
    error.config.__retryCount = error.config.__retryCount || 0
    if (error.config.__retryCount >= 1) {
      return Promise.reject(error)
    }
    error.config.__retryCount += 1
    return new Promise(resolve => {
      setTimeout(() => resolve(api(error.config)), 1000)
    })
  }
)

export default api
