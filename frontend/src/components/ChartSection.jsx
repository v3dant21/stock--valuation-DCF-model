import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'
import { BarChart3 } from 'lucide-react'

export default function ChartSection({ result }) {
  // Generate 5-year revenue projection
  const revenueData = Array.from({ length: 6 }, (_, i) => ({
    year: i === 0 ? 'Current' : `Year ${i}`,
    revenue: result.inputs.revenue * Math.pow(1 + result.inputs.revenueGrowth, i) / 1e9
  }))

  // DCF breakdown for pie chart
  const dcfData = [
    { name: 'PV of FCF', value: result.dcf.pvFcf },
    { name: 'PV Terminal Value', value: result.dcf.pvTerminalValue }
  ]

  const COLORS = ['#06b6d4', '#8b5cf6']

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Revenue Projection Chart */}
      <div className="bg-white dark:bg-[#13141a] rounded-xl border border-gray-200 dark:border-gray-800 p-6">
        <div className="flex items-center gap-3 mb-6">
          <BarChart3 className="w-5 h-5 text-cyan-500" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Revenue Projection (5 Years)
          </h3>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={revenueData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="year" stroke="#9ca3af" />
            <YAxis stroke="#9ca3af" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1a1b26', border: '1px solid #374151' }}
              labelStyle={{ color: '#fff' }}
            />
            <Bar dataKey="revenue" fill="#06b6d4" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 text-center">
          Revenue in Billions ($B)
        </p>
      </div>

      {/* Enterprise Value Breakdown */}
      <div className="bg-white dark:bg-[#13141a] rounded-xl border border-gray-200 dark:border-gray-800 p-6">
        <div className="flex items-center gap-3 mb-6">
          <BarChart3 className="w-5 h-5 text-purple-500" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Enterprise Value Breakdown
          </h3>
        </div>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={dcfData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${(entry.value / 1e9).toFixed(1)}B`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {dcfData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip 
              contentStyle={{ backgroundColor: '#1a1b26', border: '1px solid #374151' }}
              formatter={(value) => `$${(value / 1e9).toFixed(2)}B`}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
