import axios from 'axios'
import { getToken, clearAuth } from '../utils/auth'

// API base URL from environment variable
// In production, VITE_API_BASE_URL must be set
// Fallback to localhost only for development
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || (
  import.meta.env.DEV 
    ? 'http://localhost:8000/api/v1' 
    : '/api/v1'
)

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 Unauthorized - token expired or invalid
    if (error.response?.status === 401) {
      const url = error.config?.url || ''
      // Don't clear auth for login/register endpoints
      if (!url.includes('/auth/login') && !url.includes('/auth/register')) {
        clearAuth()
      }
    }
    
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    return Promise.reject(new Error(message))
  }
)

export const urlService = {
  createShortURL: async (data) => {
    const response = await api.post('/urls/', data)
    return response.data
  },

  getURLInfo: async (shortCode) => {
    const response = await api.get(`/urls/${shortCode}`)
    return response.data
  },

  listURLs: async (page = 1, pageSize = 20) => {
    const response = await api.get('/urls/', {
      params: { page, page_size: pageSize },
    })
    return response.data
  },

  deactivateURL: async (shortCode) => {
    await api.delete(`/urls/${shortCode}`)
  },
}

export const analyticsService = {
  getAnalyticsSummary: async (shortCode) => {
    const response = await api.get(`/analytics/${shortCode}/summary`)
    return response.data
  },

  getRecentClicks: async (shortCode, limit = 50) => {
    const response = await api.get(`/analytics/${shortCode}/clicks`, {
      params: { limit },
    })
    return response.data
  },
}

export const authService = {
  register: async (email, username, password) => {
    const response = await api.post('/auth/register', {
      email,
      username,
      password,
    })
    return response.data
  },

  login: async (username, password) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me')
    return response.data
  },
}

export default api

