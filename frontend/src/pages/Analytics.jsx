import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { analyticsService, urlService } from '../services/api'
import AnalyticsChart from '../components/AnalyticsChart'
import { ArrowLeft, ExternalLink, TrendingUp, Users, MousePointerClick } from 'lucide-react'
import { format } from 'date-fns'

const Analytics = () => {
  const { shortCode } = useParams()
  const navigate = useNavigate()
  const [analytics, setAnalytics] = useState(null)
  const [urlInfo, setUrlInfo] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadData()
  }, [shortCode])

  const loadData = async () => {
    setLoading(true)
    setError(null)
    try {
      const [analyticsData, urlData] = await Promise.all([
        analyticsService.getAnalyticsSummary(shortCode),
        urlService.getURLInfo(shortCode),
      ])
      setAnalytics(analyticsData)
      setUrlInfo(urlData)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card text-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Loading analytics...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card bg-red-50 border-red-200">
        <p className="text-red-700">Error: {error}</p>
        <button onClick={() => navigate('/urls')} className="btn-secondary mt-4">
          Back to URLs
        </button>
      </div>
    )
  }

  if (!analytics || !urlInfo) {
    return null
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <button
          onClick={() => navigate('/urls')}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <ArrowLeft className="h-5 w-5 text-gray-600" />
        </button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics</h1>
          <div className="flex items-center space-x-2 text-sm text-gray-600">
            <a
              href={urlInfo.short_url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:text-primary-700 font-mono flex items-center space-x-1"
            >
              <span>{urlInfo.short_url}</span>
              <ExternalLink className="h-3 w-3" />
            </a>
          </div>
          <p className="text-sm text-gray-500 mt-1 truncate">{urlInfo.original_url}</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Total Clicks</p>
              <p className="text-3xl font-bold text-gray-900">{analytics.total_clicks}</p>
            </div>
            <div className="p-3 bg-primary-100 rounded-lg">
              <MousePointerClick className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Unique Visitors</p>
              <p className="text-3xl font-bold text-gray-900">
                {analytics.unique_ips || 'N/A'}
              </p>
            </div>
            <div className="p-3 bg-primary-100 rounded-lg">
              <Users className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 mb-1">Created</p>
              <p className="text-lg font-semibold text-gray-900">
                {format(new Date(urlInfo.created_at), 'MMM d, yyyy')}
              </p>
            </div>
            <div className="p-3 bg-primary-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <AnalyticsChart
          data={analytics.clicks_by_date}
          title="Clicks by Date"
          type="date"
        />
        {analytics.clicks_by_hour && (
          <AnalyticsChart
            data={analytics.clicks_by_hour}
            title="Clicks by Hour"
            type="hour"
          />
        )}
      </div>

      {/* Top Referers */}
      {analytics.top_referers && analytics.top_referers.length > 0 && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Top Referers</h3>
          <div className="space-y-2">
            {analytics.top_referers.map((referer, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <span className="text-sm text-gray-700 truncate flex-1">
                  {referer.referer || 'Direct'}
                </span>
                <span className="text-sm font-semibold text-gray-900 ml-4">
                  {referer.count} clicks
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Analytics

