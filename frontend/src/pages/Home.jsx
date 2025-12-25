import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import URLShortener from '../components/URLShortener'
import { TrendingUp, Zap, Shield } from 'lucide-react'

const Home = () => {
  const { isAuthenticated } = useAuth()
  
  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
          Shorten Your URLs
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Create short, memorable links and track their performance with detailed analytics
        </p>
        {!isAuthenticated && (
          <div className="pt-4">
            <p className="text-sm text-gray-500 mb-4">
              Sign up to view your URLs and access analytics
            </p>
            <div className="flex items-center justify-center space-x-3">
              <Link to="/register" className="btn-primary">
                Get Started
              </Link>
              <Link to="/login" className="btn-secondary">
                Sign In
              </Link>
            </div>
          </div>
        )}
      </div>

      {/* Features */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
            <Zap className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Fast & Simple</h3>
          <p className="text-gray-600 text-sm">
            Shorten your URLs in seconds with our easy-to-use interface
          </p>
        </div>

        <div className="card text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
            <TrendingUp className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Analytics</h3>
          <p className="text-gray-600 text-sm">
            Track clicks, referrers, and engagement metrics for all your links
          </p>
        </div>

        <div className="card text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-primary-100 rounded-lg mb-4">
            <Shield className="h-6 w-6 text-primary-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure</h3>
          <p className="text-gray-600 text-sm">
            Built with security best practices and URL validation
          </p>
        </div>
      </div>

      {/* URL Shortener */}
      <URLShortener />
    </div>
  )
}

export default Home

