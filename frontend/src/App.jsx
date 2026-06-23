import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  const [activeView, setActiveView] = useState('dashboard')
  const [theme, setTheme] = useState('dark')

  return (
    <div className={`${theme} min-h-screen bg-gray-50 dark:bg-[#0a0b0d]`}>
      <div className="flex">
        <Sidebar activeView={activeView} setActiveView={setActiveView} />
        <div className="flex-1">
          <Header theme={theme} setTheme={setTheme} />
          <main className="p-6">
            {activeView === 'dashboard' && <Dashboard />}
          </main>
        </div>
      </div>
    </div>
  )
}

export default App
