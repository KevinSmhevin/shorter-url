import { useMemo } from 'react'

const AnalyticsChart = ({ data, title, type = 'bar' }) => {
  const maxValue = useMemo(() => {
    if (!data || Object.keys(data).length === 0) return 1
    return Math.max(...Object.values(data))
  }, [data])

  if (!data || Object.keys(data).length === 0) {
    return (
      <div className="card text-center py-8">
        <p className="text-gray-500">No data available</p>
      </div>
    )
  }

  const entries = Object.entries(data).sort((a, b) => {
    if (type === 'date') {
      return new Date(a[0]) - new Date(b[0])
    }
    return a[0].localeCompare(b[0])
  })

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="space-y-2">
        {entries.map(([key, value]) => (
          <div key={key} className="flex items-center space-x-3">
            <div className="w-24 text-sm text-gray-600 truncate">{key}</div>
            <div className="flex-1">
              <div className="relative h-8 bg-gray-100 rounded-lg overflow-hidden">
                <div
                  className="absolute top-0 left-0 h-full bg-primary-600 rounded-lg transition-all duration-500"
                  style={{ width: `${(value / maxValue) * 100}%` }}
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-xs font-medium text-gray-700">{value}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default AnalyticsChart

