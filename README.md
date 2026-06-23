# Stock Valuation CLI + Web Dashboard

DCF-based stock valuation calculator inspired by [Stock-Valuation](https://github.com/scfengv/Stock-Valuation).

Available as both **CLI tool** and **professional web dashboard**.

## Features

- **5-year DCF valuation** with revenue projection, EBIT, tax, reinvestment, and free cash flow
- **WACC calculation** using CAPM for cost of equity
- **Terminal value** with perpetuity growth model
- **Implied growth rate** via bisection solver (finds growth rate that matches current market price)
- **Margin of safety** analysis
- **Web Dashboard** with professional dark glassmorphism UI
- Clean separation: CLI / Web → API → Provider (data) → DCF (math) → Output

## Installation

Option 1 - Install as package (recommended):
```bash
pip install -e .
```

Then run from anywhere:
```bash
stock-valuation AAPL
```

Option 2 - Direct execution:
```bash
pip install -r requirements.txt
cd stock_valuation
python -m stock_valuation AAPL
```

## Usage

### CLI

Basic valuation:
```bash
stock-valuation AAPL
# or: python -m stock_valuation AAPL
```

With custom parameters:
```bash
stock-valuation MSFT --terminal-growth 0.03 --revenue-growth 0.08
stock-valuation GOOGL --risk-free-rate 0.045 --market-return 0.11
```

### Web Dashboard

Start the Flask API:
```bash
PYTHONPATH=src python -m stock_valuation.api
```

In another terminal, start the React frontend:
```bash
cd frontend
npm install
npm run dev
```

Access the dashboard at `http://localhost:5173`

The web interface provides:
- Interactive form for ticker and parameters
- Real-time DCF calculations
- Professional dark glassmorphism design
- Color-coded valuation metrics
- Detailed breakdown of assumptions and results

## Options

- `--terminal-growth`: Terminal growth rate (default: 2.5%)
- `--risk-free-rate`: Risk-free rate for CAPM (default: 4%)
- `--market-return`: Expected market return for CAPM (default: 10%)
- `--revenue-growth`: Revenue growth assumption (default: 10%)

## Output

The CLI displays:
- **Input Assumptions**: Revenue, margins, tax rate, growth rates, WACC components
- **Valuation Output**: Current price vs intrinsic value, margin of safety
- **Implied Growth**: Revenue growth rate priced into current market price

## Architecture

```
stock_valuation/
├── src/stock_valuation/
│   ├── cli.py         # Typer-based CLI entrypoint
│   ├── api.py         # Flask REST API for web frontend
│   ├── provider.py    # yfinance data fetching (isolated I/O)
│   ├── dcf.py         # Pure DCF calculation functions
│   ├── utils.py       # Defaults, CAPM, formatting
│   └── __main__.py    # Module execution entry
└── frontend/          # React + Vite dashboard
    ├── src/
    │   ├── App.jsx    # Main dashboard component
    │   └── ...
    └── ...
```

## Tests

```bash
PYTHONPATH=src pytest tests/ -v
```

All valuation math is tested with pure functions.

## Example Output

```
$ python -m stock_valuation AAPL

Fetching data for AAPL...

Calculating implied growth rate...

============================================================
DCF VALUATION RESULTS: AAPL
============================================================

INPUT ASSUMPTIONS:
  Revenue (TTM):           $416.16B
  EBIT Margin:             31.97%
  Tax Rate:                15.61%
  Reinvestment Rate:       0.24%
  Revenue Growth:          10.00%
  Terminal Growth:         2.50%
  WACC:                    10.43%
    - Cost of Equity:      10.52%
    - Cost of Debt:        5.00%
    - Equity Weight:       98.59%
    - Debt Weight:         1.41%
  Beta:                    1.09

VALUATION OUTPUT:
  Current Price:           $298.01
  Intrinsic Value:         $134.41
  Margin of Safety:        -121.72%
  → Stock is OVERVALUED by 121.72%

IMPLIED GROWTH:
  Implied Revenue Growth:  31.08%
  → Market is pricing in 31.08% revenue growth

============================================================
```
