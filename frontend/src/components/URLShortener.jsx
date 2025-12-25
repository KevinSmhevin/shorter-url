import { useState } from 'react'
import { useURL } from '../contexts/URLContext'
import { useAuth } from '../contexts/AuthContext'
import { Copy, Check, ExternalLink, Calendar } from 'lucide-react'
import { format } from 'date-fns'

const URLShortener = () => {
  const { createShortURL, fetchURLs, loading, error } = useURL()
  const { isAuthenticated } = useAuth()
  const [originalUrl, setOriginalUrl] = useState('')
  const [customCode, setCustomCode] = useState('')
  const [expiresInDays, setExpiresInDays] = useState('')
  const [createdURL, setCreatedURL] = useState(null)
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setCreatedURL(null)

    try {
      const data = {
        original_url: originalUrl,
        ...(customCode && { custom_code: customCode }),
        ...(expiresInDays && { expires_in_days: parseInt(expiresInDays) }),
      }

      const result = await createShortURL(data)
      setCreatedURL(result)
      setOriginalUrl('')
      setCustomCode('')
      setExpiresInDays('')
      
      // If user is authenticated, refresh the URL list to show the new URL
      if (isAuthenticated) {
        await fetchURLs()
      }
    } catch (err) {
      // Error is handled by context
    }
  }

  const handleCopy = async () => {
    if (createdURL?.short_url) {
      await navigator.clipboard.writeText(createdURL.short_url)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Shorten Your URL</h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="originalUrl" className="block text-sm font-medium text-gray-700 mb-2">
            Enter your long URL
          </label>
          <input
            id="originalUrl"
            type="url"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
            placeholder="https://example.com/very/long/url"
            className="input-field"
            required
            disabled={loading}
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="customCode" className="block text-sm font-medium text-gray-700 mb-2">
              Custom Code (optional)
            </label>
            <input
              id="customCode"
              type="text"
              value={customCode}
              onChange={(e) => setCustomCode(e.target.value)}
              placeholder="my-custom-link"
              className="input-field"
              pattern="[A-Za-z0-9]+"
              minLength={4}
              maxLength={20}
              disabled={loading}
            />
            <p className="mt-1 text-xs text-gray-500">4-20 alphanumeric characters</p>
          </div>

          <div>
            <label htmlFor="expiresInDays" className="block text-sm font-medium text-gray-700 mb-2">
              Expires in (days, optional)
            </label>
            <input
              id="expiresInDays"
              type="number"
              value={expiresInDays}
              onChange={(e) => setExpiresInDays(e.target.value)}
              placeholder="30"
              className="input-field"
              min="1"
              max="365"
              disabled={loading}
            />
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !originalUrl}
          className="btn-primary w-full"
        >
          {loading ? 'Creating...' : 'Shorten URL'}
        </button>
      </form>

      {createdURL && (
        <div className="mt-6 p-4 bg-primary-50 border border-primary-200 rounded-lg">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Short URL:</span>
            <button
              onClick={handleCopy}
              className="flex items-center space-x-1 text-primary-600 hover:text-primary-700 text-sm"
            >
              {copied ? (
                <>
                  <Check className="h-4 w-4" />
                  <span>Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="h-4 w-4" />
                  <span>Copy</span>
                </>
              )}
            </button>
          </div>
          <div className="flex items-center space-x-2">
            <a
              href={createdURL.short_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 font-mono text-sm break-all flex items-center space-x-1"
            >
              <span>{createdURL.short_url}</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
          <div className="mt-3 pt-3 border-t border-primary-200">
            <div className="flex items-center space-x-4 text-xs text-gray-600">
              <div className="flex items-center space-x-1">
                <Calendar className="h-3 w-3" />
                <span>Created: {format(new Date(createdURL.created_at), 'MMM d, yyyy')}</span>
              </div>
              {createdURL.expires_at && (
                <div className="flex items-center space-x-1">
                  <Calendar className="h-3 w-3" />
                  <span>Expires: {format(new Date(createdURL.expires_at), 'MMM d, yyyy')}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default URLShortener

