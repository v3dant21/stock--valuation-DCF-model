import { Calculator } from 'lucide-react'

export default function ValuationForm({ 
  ticker, setTicker, 
  revenueGrowth, setRevenueGrowth,
  terminalGrowth, setTerminalGrowth,
  loading, error, onCalculate 
}) {
  const formatPercent = (value) => `${(value * 100).toFixed(2)}%`

  return (
    <div className="bg-white dark:bg-[#13141a] rounded-xl border border-gray-200 dark:border-gray-800 p-6">
      <div className="flex items-center gap-3 mb-6">
        <Calculator className="w-6 h-6 text-cyan-500" />
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
          Valuation Calculator
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Ticker Symbol
          </label>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
            placeholder="AAPL"
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-[#1a1b26] border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors uppercase"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Revenue Growth
          </label>
          <input
            type="number"
            value={revenueGrowth}
            onChange={(e) => setRevenueGrowth(parseFloat(e.target.value))}
            step="0.01"
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-[#1a1b26] border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-cyan-500 transition-colors"
          />
          <p className="text-xs text-gray-500 mt-1">{formatPercent(revenueGrowth)}</p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Terminal Growth
          </label>
          <input
            type="number"
            value={terminalGrowth}
            onChange={(e) => setTerminalGrowth(parseFloat(e.target.value))}
            step="0.01"
            className="w-full px-4 py-2.5 bg-gray-50 dark:bg-[#1a1b26] border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white focus:outline-none focus:border-cyan-500 transition-colors"
          />
          <p className="text-xs text-gray-500 mt-1">{formatPercent(terminalGrowth)}</p>
        </div>

        <div className="flex items-end">
          <button
            onClick={onCalculate}
            disabled={loading || !ticker}
            className="w-full px-6 py-2.5 bg-cyan-600 hover:bg-cyan-500 disabled:bg-gray-700 disabled:text-gray-500 text-white font-medium rounded-lg transition-all duration-200"
          >
            {loading ? 'Analyzing...' : 'Calculate'}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 bg-red-900/20 border border-red-800 rounded-lg text-red-400 text-sm">
          {error}
        </div>
      )}
    </div>
  )
}
