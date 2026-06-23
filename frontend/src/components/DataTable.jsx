import { Table } from 'lucide-react'

export default function DataTable({ result }) {
  const formatCurrency = (value) => {
    if (value >= 1e9) return `$${(value / 1e9).toFixed(2)}B`
    if (value >= 1e6) return `$${(value / 1e6).toFixed(2)}M`
    return `$${value.toFixed(2)}`
  }

  const formatPercent = (value) => `${(value * 100).toFixed(2)}%`

  const inputData = [
    { category: 'Revenue', metric: 'TTM Revenue', value: formatCurrency(result.inputs.revenue) },
    { category: 'Margins', metric: 'EBIT Margin', value: formatPercent(result.inputs.ebitMargin) },
    { category: 'Tax', metric: 'Effective Tax Rate', value: formatPercent(result.inputs.taxRate) },
    { category: 'Growth', metric: 'Revenue Growth', value: formatPercent(result.inputs.revenueGrowth) },
    { category: 'Growth', metric: 'Terminal Growth', value: formatPercent(result.inputs.terminalGrowth) },
    { category: 'WACC', metric: 'Cost of Capital', value: formatPercent(result.inputs.wacc) },
    { category: 'WACC', metric: 'Cost of Equity', value: formatPercent(result.inputs.costOfEquity) },
    { category: 'WACC', metric: 'Cost of Debt', value: formatPercent(result.inputs.costOfDebt) },
    { category: 'Risk', metric: 'Beta', value: result.inputs.beta.toFixed(3) },
    { category: 'Capital', metric: 'Reinvestment Rate', value: formatPercent(result.inputs.reinvestmentRate) },
    { category: 'Structure', metric: 'Equity Weight', value: formatPercent(result.inputs.equityWeight) },
    { category: 'Structure', metric: 'Debt Weight', value: formatPercent(result.inputs.debtWeight) },
  ]

  const dcfData = [
    { metric: 'PV of Free Cash Flows', value: formatCurrency(result.dcf.pvFcf) },
    { metric: 'PV of Terminal Value', value: formatCurrency(result.dcf.pvTerminalValue) },
    { metric: 'Enterprise Value', value: formatCurrency(result.dcf.enterpriseValue) },
    { metric: 'Intrinsic Value per Share', value: `$${result.intrinsicValue.toFixed(2)}` },
  ]

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Input Assumptions Table */}
      <div className="bg-white dark:bg-[#13141a] rounded-xl border border-gray-200 dark:border-gray-800 p-6">
        <div className="flex items-center gap-3 mb-6">
          <Table className="w-5 h-5 text-cyan-500" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Input Assumptions
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200 dark:border-gray-800">
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Category</th>
                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Metric</th>
                <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700 dark:text-gray-300">Value</th>
              </tr>
            </thead>
            <tbody>
              {inputData.map((row, i) => (
                <tr key={i} className="border-b border-gray-100 dark:border-gray-800/50 hover:bg-gray-50 dark:hover:bg-gray-800/30 transition-colors">
                  <td className="py-3 px-4 text-sm text-gray-600 dark:text-gray-400">{row.category}</td>
                  <td className="py-3 px-4 text-sm text-gray-900 dark:text-white">{row.metric}</td>
                  <td className="py-3 px-4 text-sm text-gray-900 dark:text-white text-right font-medium">{row.value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* DCF Results Table */}
      <div className="bg-white dark:bg-[#13141a] rounded-xl border border-gray-200 dark:border-gray-800 p-6">
        <div className="flex items-center gap-3 mb-6">
          <Table className="w-5 h-5 text-purple-500" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            DCF Results
          </h3>
        </div>
        <div className="space-y-4">
          {dcfData.map((row, i) => (
            <div key={i} className="flex justify-between items-center py-4 border-b border-gray-100 dark:border-gray-800 last:border-0">
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{row.metric}</span>
              <span className="text-lg font-bold text-gray-900 dark:text-white">{row.value}</span>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-cyan-500/10 dark:bg-cyan-500/20 rounded-lg border border-cyan-500/20">
          <div className="flex justify-between items-center">
            <span className="text-sm font-semibold text-cyan-700 dark:text-cyan-400">Market Price vs Intrinsic</span>
            <span className={`text-lg font-bold ${result.marginOfSafety > 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
              {result.marginOfSafety > 0 ? '↓' : '↑'} {Math.abs(result.marginOfSafety * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
