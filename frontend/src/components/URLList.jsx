import { useState, useEffect } from 'react'
import { useURL } from '../contexts/URLContext'
import { Copy, Check, ExternalLink, Trash2, BarChart3, Calendar } from 'lucide-react'
import { format } from 'date-fns'
import { useNavigate } from 'react-router-dom'

const URLList = () => {
  const { urls, loading, error, fetchURLs, deactivateURL } = useURL()
  const [page, setPage] = useState(1)
  const [pageSize] = useState(20)
  const [totalPages, setTotalPages] = useState(1)
  const [copiedCode, setCopiedCode] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const loadURLs = async () => {
      try {
        const data = await fetchURLs(page, pageSize)
        setTotalPages(data.total_pages || 1)
      } catch (err) {
        // Error handled by context
      }
    }
    loadURLs()
  }, [page, pageSize, fetchURLs])

  const handleCopy = async (shortUrl) => {
    await navigator.clipboard.writeText(shortUrl)
    setCopiedCode(shortUrl)
    setTimeout(() => setCopiedCode(null), 2000)
  }

  const handleDeactivate = async (shortCode) => {
    if (window.confirm('Are you sure you want to deactivate this URL?')) {
      try {
        await deactivateURL(shortCode)
      } catch (err) {
        // Error handled by context
      }
    }
  }

  if (loading && urls.length === 0) {
    return (
      <div className="card text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading URLs...</p>
      </div>
    )
  }

  if (error && urls.length === 0) {
    return (
      <div className="card bg-red-50 border-red-200">
        <p className="text-red-700">Error: {error}</p>
      </div>
    )
  }

  if (urls.length === 0) {
    return (
      <div className="card text-center py-12">
        <p className="text-gray-600">No URLs found. Create your first shortened URL!</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {urls.map((url) => (
        <div key={url.id} className="card hover:shadow-md transition-shadow">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-2 mb-2">
                <a
                  href={url.short_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary-600 hover:text-primary-700 font-mono text-sm font-medium flex items-center space-x-1"
                >
                  <span>{url.short_url}</span>
                  <ExternalLink className="h-3 w-3" />
                </a>
                <button
                  onClick={() => handleCopy(url.short_url)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  {copiedCode === url.short_url ? (
                    <Check className="h-4 w-4 text-green-600" />
                  ) : (
                    <Copy className="h-4 w-4" />
                  )}
                </button>
              </div>
              <p className="text-sm text-gray-600 truncate">{url.original_url}</p>
              <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                <div className="flex items-center space-x-1">
                  <Calendar className="h-3 w-3" />
                  <span>{format(new Date(url.created_at), 'MMM d, yyyy')}</span>
                </div>
                <span>•</span>
                <span>{url.click_count} clicks</span>
                {url.expires_at && (
                  <>
                    <span>•</span>
                    <span>Expires: {format(new Date(url.expires_at), 'MMM d, yyyy')}</span>
                  </>
                )}
                {!url.is_active && (
                  <span className="text-red-600 font-medium">• Inactive</span>
                )}
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => navigate(`/analytics/${url.short_code}`)}
                className="btn-secondary flex items-center space-x-1 text-sm"
              >
                <BarChart3 className="h-4 w-4" />
                <span>Analytics</span>
              </button>
              <button
                onClick={() => handleDeactivate(url.short_code)}
                className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                title="Deactivate"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      ))}

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex justify-center items-center space-x-2 mt-6">
          <button
            onClick={() => setPage((p) => Math.max(1, p - 1))}
            disabled={page === 1}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <span className="text-sm text-gray-600">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      )}
    </div>
  )
}

export default URLList

