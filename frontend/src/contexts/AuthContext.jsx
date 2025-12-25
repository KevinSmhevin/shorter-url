import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { authService } from '../services/api'
import { setToken, getToken, setUser, getUser, clearAuth } from '../utils/auth'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUserState] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  // Initialize auth state from localStorage
  useEffect(() => {
    const initializeAuth = async () => {
      const token = getToken()
      const storedUser = getUser()
      
      if (token && storedUser) {
        // Set user from storage immediately for fast UI
        setUserState(storedUser)
        
        // Verify token is still valid with backend
        try {
          const userData = await authService.getCurrentUser()
          setUserState(userData)
          setUser(userData)
        } catch (err) {
          // Token invalid, clear everything
          clearAuth()
          setUserState(null)
        }
      }
      
      setLoading(false)
    }
    
    initializeAuth()
  }, [])

  // Shared authentication success handler
  const handleAuthSuccess = useCallback((response) => {
    if (!response?.access_token) {
      throw new Error('Authentication failed: No token received')
    }
    
    setToken(response.access_token)
    const userData = response.user || null
    
    if (userData) {
      setUserState(userData)
      setUser(userData)
    }
    
    return userData
  }, [])

  const login = useCallback(async (username, password) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await authService.login(username, password)
      const userData = handleAuthSuccess(response)
      
      // If user not in response, fetch it
      if (!userData) {
        const fetchedUser = await authService.getCurrentUser()
        setUserState(fetchedUser)
        setUser(fetchedUser)
        return fetchedUser
      }
      
      return userData
    } catch (err) {
      const errorMessage = err.message || 'Login failed'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [handleAuthSuccess])

  const register = useCallback(async (email, username, password) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await authService.register(email, username, password)
      const userData = handleAuthSuccess(response)
      
      // If user not in response, fetch it
      if (!userData) {
        const fetchedUser = await authService.getCurrentUser()
        setUserState(fetchedUser)
        setUser(fetchedUser)
        return fetchedUser
      }
      
      return userData
    } catch (err) {
      const errorMessage = err.message || 'Registration failed'
      setError(errorMessage)
      throw err
    } finally {
      setLoading(false)
    }
  }, [handleAuthSuccess])

  const logout = useCallback(() => {
    clearAuth()
    setUserState(null)
    setError(null)
  }, [])

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
