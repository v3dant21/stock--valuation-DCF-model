# Stock Valuation Frontend

Professional React dashboard for DCF stock valuation.

## Features

- **Dark Glassmorphism Design** - Modern gradient background with backdrop blur cards
- **Real-time Valuation** - Instant DCF calculations via Flask API
- **Color-coded Metrics** - Visual indicators for undervalued/overvalued stocks
- **Responsive Layout** - Works on desktop and mobile
- **Professional UI/UX** - Following financial dashboard best practices

## Setup

```bash
# Install dependencies
npm install

# Start dev server
npm run dev
```

The app runs on `http://localhost:5173`

## Backend

The backend Flask API must be running on port 5000:

```bash
cd ..
PYTHONPATH=src python -m stock_valuation.api
```

## Usage

1. Enter a ticker symbol (e.g., AAPL, MSFT, GOOGL)
2. Adjust revenue growth and terminal growth assumptions
3. Click "Calculate Valuation"
4. View intrinsic value, margin of safety, and implied growth rate

## Tech Stack

- React 18
- Vite
- Tailwind CSS
- Modern gradient + glassmorphism styling

## Design

The UI follows professional financial dashboard patterns:
- Dark mode with high contrast for readability
- Gradient accents for visual hierarchy
- Backdrop blur for depth
- Color coding: Blue (neutral), Green (positive), Red (negative)
- Smooth transitions (200ms)
- Clear typography with proper spacing
