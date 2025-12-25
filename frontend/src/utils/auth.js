/**
 * Authentication utility functions
 * Centralized token management following best practices
 */

const TOKEN_KEY = 'access_token'
const USER_KEY = 'user'

/**
 * Store authentication token
 */
export const setToken = (token) => {
  if (token) {
    try {
      localStorage.setItem(TOKEN_KEY, token)
    } catch (error) {
      // localStorage may be disabled or full - fail silently
      return false
    }
  }
  return false
}

/**
 * Get authentication token
 */
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * Remove authentication token
 */
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY)
}

/**
 * Store user data
 */
export const setUser = (user) => {
  if (user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  }
}

/**
 * Get user data
 */
export const getUser = () => {
  const userStr = localStorage.getItem(USER_KEY)
  if (userStr) {
    try {
      return JSON.parse(userStr)
    } catch {
      return null
    }
  }
  return null
}

/**
 * Remove user data
 */
export const removeUser = () => {
  localStorage.removeItem(USER_KEY)
}

/**
 * Clear all authentication data
 */
export const clearAuth = () => {
  removeToken()
  removeUser()
}

/**
 * Check if user is authenticated (has token)
 */
export const isAuthenticated = () => {
  return !!getToken()
}

