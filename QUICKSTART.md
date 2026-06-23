# Quick Start Guide

## Installation

```bash
cd stock_valuation
pip install -e .
```

## Basic Usage

Analyze a stock with default parameters (10% revenue growth, 2.5% terminal growth):
```bash
stock-valuation AAPL
```

## Advanced Usage

Customize valuation parameters:
```bash
# High growth stock
stock-valuation NVDA --revenue-growth 0.25 --terminal-growth 0.03

# Conservative valuation
stock-valuation KO --revenue-growth 0.05 --terminal-growth 0.02

# Custom risk parameters
stock-valuation TSLA --risk-free-rate 0.045 --market-return 0.12
```

## Understanding the Output

### Input Assumptions
- **Revenue (TTM)**: Trailing twelve months revenue
- **EBIT Margin**: Operating profit margin
- **Tax Rate**: Effective tax rate from financials
- **Reinvestment Rate**: Calculated from capex and depreciation
- **WACC**: Weighted average cost of capital (uses CAPM for equity cost)

### Valuation Output
- **Current Price**: Market price per share
- **Intrinsic Value**: DCF-calculated fair value
- **Margin of Safety**: (Intrinsic - Current) / Intrinsic
  - Positive = undervalued
  - Negative = overvalued

### Implied Growth
- The revenue growth rate that would justify the current market price
- If implied growth > assumed growth → market is more optimistic
- If implied growth < assumed growth → market is more pessimistic

## Tips

1. **Always verify the inputs**: Check if EBIT margin and tax rate make sense
2. **Adjust for sector**: High-tech stocks need higher growth assumptions
3. **Compare implied vs assumed growth**: Shows market expectations
4. **Use multiple scenarios**: Test different growth rates to see sensitivity
5. **Consider qualitative factors**: DCF is just one tool in valuation

## Common Parameters

| Sector | Revenue Growth | Terminal Growth | Notes |
|--------|----------------|-----------------|-------|
| Tech Growth | 15-25% | 3-4% | High initial, moderate terminal |
| Mature Tech | 8-12% | 2-3% | Stable large cap |
| Consumer Staples | 3-6% | 2% | Low growth, defensive |
| Healthcare | 6-10% | 2.5% | Moderate growth |
| Financials | 5-8% | 2% | GDP-linked |

## Troubleshooting

**Error: Could not fetch data**
- Check ticker symbol is correct
- Verify internet connection
- Some tickers may not have complete financial data

**Unrealistic valuation**
- Adjust revenue growth assumption
- Check if EBIT margin is abnormal
- Consider using sector-specific parameters
