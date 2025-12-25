import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { Link2, Home, LogOut, User, Menu, X } from 'lucide-react'
import { useAuth } from '../contexts/AuthContext'

const Layout = ({ children }) => {
  const location = useLocation()
  const navigate = useNavigate()
  const { user, logout, isAuthenticated } = useAuth()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  const isActive = (path) => {
    return location.pathname === path
  }

  const handleLogout = () => {
    logout()
    navigate('/')
    setMobileMenuOpen(false)
  }

  const NavLink = ({ to, icon: Icon, children, onClick }) => {
    const active = isActive(to)
    const baseClasses = "flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
    const activeClasses = active ? "bg-primary-100 text-primary-700" : "text-gray-600 hover:bg-gray-100"
    
    if (onClick) {
      return (
        <button onClick={onClick} className={`${baseClasses} ${activeClasses} w-full text-left`}>
          <Icon className="h-4 w-4" />
          <span>{children}</span>
        </button>
      )
    }
    
    return (
      <Link
        to={to}
        onClick={() => setMobileMenuOpen(false)}
        className={`${baseClasses} ${activeClasses}`}
      >
        <Icon className="h-4 w-4" />
        <span>{children}</span>
      </Link>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-2" onClick={() => setMobileMenuOpen(false)}>
              <Link2 className="h-6 w-6 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">ShortURL</span>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden md:flex items-center space-x-1">
              <NavLink to="/" icon={Home}>Home</NavLink>
              {isAuthenticated && (
                <NavLink to="/urls" icon={Link2}>My URLs</NavLink>
              )}
              {isAuthenticated ? (
                <>
                  <div className="flex items-center space-x-2 ml-2 pl-2 border-l border-gray-200">
                    <div className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-700">
                      <User className="h-4 w-4" />
                      <span className="font-medium">{user?.username}</span>
                    </div>
                    <button
                      onClick={handleLogout}
                      className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors flex items-center space-x-2"
                    >
                      <LogOut className="h-4 w-4" />
                      <span>Logout</span>
                    </button>
                  </div>
                </>
              ) : (
                <div className="flex items-center space-x-2 ml-2">
                  <Link
                    to="/login"
                    className="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors"
                  >
                    Sign In
                  </Link>
                  <Link
                    to="/register"
                    className="btn-primary text-sm"
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </div>

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </button>
          </div>

          {/* Mobile Navigation Menu */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t border-gray-200 py-2">
              <div className="flex flex-col space-y-1">
                <NavLink to="/" icon={Home}>Home</NavLink>
                {isAuthenticated && (
                  <NavLink to="/urls" icon={Link2}>My URLs</NavLink>
                )}
                {isAuthenticated ? (
                  <>
                    <div className="flex items-center space-x-2 px-3 py-2 text-sm text-gray-700 border-t border-gray-200 mt-1 pt-2">
                      <User className="h-4 w-4" />
                      <span className="font-medium">{user?.username}</span>
                    </div>
                    <NavLink icon={LogOut} onClick={handleLogout}>Logout</NavLink>
                  </>
                ) : (
                  <>
                    <div className="flex flex-col space-y-2 border-t border-gray-200 mt-1 pt-2">
                      <Link
                        to="/login"
                        onClick={() => setMobileMenuOpen(false)}
                        className="px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors text-center"
                      >
                        Sign In
                      </Link>
                      <Link
                        to="/register"
                        onClick={() => setMobileMenuOpen(false)}
                        className="btn-primary text-sm text-center"
                      >
                        Sign Up
                      </Link>
                    </div>
                  </>
                )}
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-500">
            © 2024 ShortURL. Built with FastAPI and React.
          </p>
        </div>
      </footer>
    </div>
  )
}

export default Layout

