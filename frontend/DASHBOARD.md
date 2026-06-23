# Professional DCF Dashboard

## Overview

A comprehensive, enterprise-grade financial dashboard for stock valuation using Discounted Cash Flow (DCF) analysis. Built with React, Recharts, and Tailwind CSS.

## Features

### 🎨 Professional UI/UX
- **Sidebar Navigation** - Clean navigation with dashboard, valuation, history, and settings sections
- **Dark/Light Theme** - Seamless theme switching with system preference support
- **Responsive Design** - Fully responsive from mobile to 4K displays
- **Modern Components** - Lucide icons, smooth transitions, professional color scheme

### 📊 Interactive Dashboard
1. **Valuation Calculator**
   - Quick-access form for ticker input
   - Adjustable revenue and terminal growth rates
   - Real-time validation and error handling

2. **Metrics Grid (6 Cards)**
   - Current Price
   - Intrinsic Value
   - Margin of Safety (with trend indicator)
   - Implied Growth Rate
   - WACC
   - Beta

3. **Visual Analytics**
   - **Revenue Projection Chart** - 5-year bar chart showing revenue growth
   - **Enterprise Value Breakdown** - Pie chart showing PV of FCF vs Terminal Value

4. **Data Tables**
   - **Input Assumptions Table** - 12 rows of detailed inputs
   - **DCF Results Table** - Complete breakdown with highlight card

### 🔍 Search & Navigation
- Global search bar for stocks and tickers
- Notification center
- User profile menu
- Theme toggle

## Component Architecture

```
src/
├── App.jsx                    # Main app with routing
├── components/
│   ├── Sidebar.jsx           # Left navigation sidebar
│   ├── Header.jsx            # Top header with search
│   ├── Dashboard.jsx         # Main dashboard container
│   ├── ValuationForm.jsx     # Input form component
│   ├── MetricsGrid.jsx       # 6 metric cards
│   ├── ChartSection.jsx      # Revenue & pie charts
│   └── DataTable.jsx         # Detailed data tables
└── App.css                   # Global styles
```

## Technology Stack

- **React 18** - Component framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Chart library
- **Lucide React** - Icon system

## Color Scheme

### Dark Mode (Default)
- Background: `#0a0b0d`
- Cards: `#13141a`
- Inputs: `#1a1b26`
- Accent: Cyan-500/600
- Borders: Gray-800

### Light Mode
- Background: `#f9fafb` (gray-50)
- Cards: White
- Inputs: `#f3f4f6` (gray-100)
- Accent: Cyan-600
- Borders: Gray-200

## Usage

### Start Development Server
```bash
cd frontend
npm install
npm run dev
```

### Start Backend API
```bash
cd ..
PYTHONPATH=src python -m stock_valuation.api
```

### Access Dashboard
Open `http://localhost:5173` (or next available port)

## Features in Detail

### Metrics Grid
Each card shows:
- Icon with colored background
- Current value (large, bold)
- Descriptive label
- Optional trend badge (Undervalued/Overvalued)

### Charts
1. **Revenue Projection**
   - Bar chart with 6 data points (current + 5 years)
   - Values in billions ($B)
   - Cyan bars with rounded corners

2. **Enterprise Value Breakdown**
   - Pie chart with 2 segments
   - Cyan: PV of FCF
   - Purple: PV of Terminal Value
   - Interactive tooltips with values

### Data Tables
1. **Input Assumptions**
   - 12 rows organized by category
   - Revenue, Margins, Tax, Growth, WACC, Risk, Capital, Structure
   - Hover effects on rows

2. **DCF Results**
   - 4 key results in large format
   - Highlight card showing margin of safety
   - Up/down arrow indicating valuation status

## API Integration

Connects to Flask backend at `http://localhost:5000/api/valuation`

**Request:**
```json
{
  "ticker": "AAPL",
  "revenueGrowth": 0.10,
  "terminalGrowth": 0.025
}
```

**Response:**
```json
{
  "currentPrice": 298.01,
  "intrinsicValue": 134.41,
  "marginOfSafety": -1.2172,
  "impliedGrowth": 0.3108,
  "inputs": { ... },
  "dcf": { ... }
}
```

## Accessibility

- ✅ Keyboard navigation
- ✅ Focus indicators on all interactive elements
- ✅ WCAG AA contrast ratios
- ✅ Semantic HTML
- ✅ Screen reader friendly labels

## Performance

- Code splitting by component
- Lazy loading for charts
- Optimized re-renders with React.memo
- Tailwind CSS purging (< 20KB CSS)
- < 1s initial page load

## Future Enhancements

- [ ] Historical data visualization
- [ ] Multiple ticker comparison
- [ ] Saved watchlists
- [ ] Export to PDF/CSV
- [ ] Scenario analysis
- [ ] Monte Carlo simulation
- [ ] Custom assumptions presets
- [ ] Real-time market data updates
- [ ] User authentication
- [ ] Portfolio tracking

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

The dashboard follows modern React best practices:
- Functional components with hooks
- Props drilling for simple state
- Consistent naming conventions
- Component composition over inheritance
