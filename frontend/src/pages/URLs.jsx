import { useEffect } from 'react'
import { useURL } from '../contexts/URLContext'
import { useAuth } from '../contexts/AuthContext'
import URLList from '../components/URLList'

const URLs = () => {
  const { fetchURLs } = useURL()
  const { isAuthenticated, loading } = useAuth()

  useEffect(() => {
    if (!loading && isAuthenticated) {
      fetchURLs().catch(() => {
        // Error handled by URLContext
      })
    }
  }, [isAuthenticated, loading, fetchURLs])

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">My URLs</h1>
        <p className="text-gray-600">Manage and track all your shortened URLs</p>
      </div>
      <URLList />
    </div>
  )
}

export default URLs

