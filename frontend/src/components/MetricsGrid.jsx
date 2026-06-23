import { DollarSign, Target, TrendingUp, TrendingDown, Activity, Percent } from 'lucide-react'

export default function MetricsGrid({ result }) {
  const formatCurrency = (value) => {
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`
    if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`
    return `$${value.toFixed(2)}`
  }

  const formatPercent = (value) => `${(value * 100).toFixed(2)}%`

  const metrics = [
    {
      label: 'Current Price',
      value: `$${result.currentPrice.toFixed(2)}`,
      icon: DollarSign,
      color: 'blue',
      trend: null
    },
    {
      label: 'Intrinsic Value',
      value: `$${result.intrinsicValue.toFixed(2)}`,
      icon: Target,
      color: 'green',
      trend: null
    },
    {
      label: 'Margin of Safety',
      value: formatPercent(Math.abs(result.marginOfSafety)),
      icon: result.marginOfSafety > 0 ? TrendingUp : TrendingDown,
      color: result.marginOfSafety > 0 ? 'green' : 'red',
      trend: result.marginOfSafety > 0 ? 'Undervalued' : 'Overvalued'
    },
    {
      label: 'Implied Growth',
      value: result.impliedGrowth ? formatPercent(result.impliedGrowth) : 'N/A',
      icon: Activity,
      color: 'purple',
      trend: null
    },
    {
      label: 'WACC',
      value: formatPercent(result.inputs.wacc),
      icon: Percent,
      color: 'orange',
      trend: null
    },
    {
      label: 'Beta',
      value: result.inputs.beta.toFixed(2),
      icon: Activity,
      color: 'pink',
      trend: null
    }
  ]

  const colorClasses = {
    blue: 'bg-blue-500/10 text-blue-500 dark:bg-blue-500/20',
    green: 'bg-green-500/10 text-green-500 dark:bg-green-500/20',
    red: 'bg-red-500/10 text-red-500 dark:bg-red-500/20',
    purple: 'bg-purple-500/10 text-purple-500 dark:bg-purple-500/20',
    orange: 'bg-orange-500/10 text-orange-500 dark:bg-orange-500/20',
    pink: 'bg-pink-500/10 text-pink-500 dark:bg-pink-500/20'
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {metrics.map((metric, i) => (
        <div key={i} className="bg-white dark:bg-[#13141a] rounded-xl border border-gray-200 dark:border-gray-800 p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-start justify-between mb-4">
            <div className={`p-3 rounded-lg ${colorClasses[metric.color]}`}>
              <metric.icon className="w-6 h-6" />
            </div>
            {metric.trend && (
              <span className={`text-xs font-medium px-2 py-1 rounded ${
                metric.color === 'green' ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
              }`}>
                {metric.trend}
              </span>
            )}
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{metric.label}</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{metric.value}</p>
        </div>
      ))}
    </div>
  )
}
