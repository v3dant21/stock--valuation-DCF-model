import { useState } from 'react'
import { TrendingUp, TrendingDown, DollarSign, Target, BarChart3, Calculator } from 'lucide-react'
import ValuationForm from './ValuationForm'
import MetricsGrid from './MetricsGrid'
import ChartSection from './ChartSection'
import DataTable from './DataTable'

export default function Dashboard() {
  const [ticker, setTicker] = useState('')
  const [revenueGrowth, setRevenueGrowth] = useState(0.10)
  const [terminalGrowth, setTerminalGrowth] = useState(0.025)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleCalculate = async () => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch('http://localhost:5000/api/valuation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ticker: ticker.toUpperCase(),
          revenueGrowth,
          terminalGrowth,
        }),
      })

      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch valuation')
      }

      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          DCF Valuation Dashboard
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Professional discounted cash flow analysis with real-time market data
        </p>
      </div>

      <ValuationForm
        ticker={ticker}
        setTicker={setTicker}
        revenueGrowth={revenueGrowth}
        setRevenueGrowth={setRevenueGrowth}
        terminalGrowth={terminalGrowth}
        setTerminalGrowth={setTerminalGrowth}
        loading={loading}
        error={error}
        onCalculate={handleCalculate}
      />

      {result && (
        <>
          <MetricsGrid result={result} />
          <ChartSection result={result} />
          <DataTable result={result} />
        </>
      )}
    </div>
  )
}
