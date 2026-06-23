import { LayoutDashboard, TrendingUp, History, Settings } from 'lucide-react'

export default function Sidebar({ activeView, setActiveView }) {
  const menuItems = [
    { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { id: 'valuation', icon: TrendingUp, label: 'Valuation' },
    { id: 'history', icon: History, label: 'History' },
    { id: 'settings', icon: Settings, label: 'Settings' },
  ]

  return (
    <aside className="w-64 bg-white dark:bg-[#13141a] border-r border-gray-200 dark:border-gray-800 h-screen sticky top-0">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-lg flex items-center justify-center text-white font-bold text-xl">
            $
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900 dark:text-white">DCF Pro</h1>
            <p className="text-xs text-gray-500 dark:text-gray-400">Valuation Platform</p>
          </div>
        </div>

        <nav className="space-y-2">
          {menuItems.map(item => (
            <button
              key={item.id}
              onClick={() => setActiveView(item.id)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                activeView === item.id
                  ? 'bg-cyan-500 text-white'
                  : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>
    </aside>
  )
}
