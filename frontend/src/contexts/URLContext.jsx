import { createContext, useContext, useState, useCallback } from 'react'
import { urlService } from '../services/api'

const URLContext = createContext()

export const useURL = () => {
  const context = useContext(URLContext)
  if (!context) {
    throw new Error('useURL must be used within a URLProvider')
  }
  return context
}

export const URLProvider = ({ children }) => {
  const [urls, setUrls] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchURLs = useCallback(async (page = 1, pageSize = 20) => {
    setLoading(true)
    setError(null)
    try {
      const data = await urlService.listURLs(page, pageSize)
      setUrls(data.urls)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const createShortURL = useCallback(async (data) => {
    setLoading(true)
    setError(null)
    try {
      const newURL = await urlService.createShortURL(data)
      setUrls((prev) => [newURL, ...prev])
      return newURL
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const deactivateURL = useCallback(async (shortCode) => {
    setLoading(true)
    setError(null)
    try {
      await urlService.deactivateURL(shortCode)
      setUrls((prev) => prev.filter((url) => url.short_code !== shortCode))
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }, [])

  const value = {
    urls,
    loading,
    error,
    createShortURL,
    fetchURLs,
    deactivateURL,
  }

  return <URLContext.Provider value={value}>{children}</URLContext.Provider>
}

