"""Flask API server for stock valuation."""
from flask import Flask, request, jsonify
from flask_cors import CORS
from stock_valuation.provider import DataProvider
from stock_valuation.dcf import dcf_valuation, margin_of_safety, find_implied_growth
from stock_valuation.utils import (
    get_default_risk_free_rate,
    get_default_market_return,
    get_default_terminal_growth,
    calculate_cost_of_equity,
    estimate_reinvestment_rate,
)

app = Flask(__name__)
CORS(app)


@app.route("/api/valuation", methods=["POST"])
def calculate_valuation():
    """Calculate DCF valuation for a ticker."""
    try:
        data = request.get_json()
        ticker = data.get("ticker")
        
        if not ticker:
            return jsonify({"error": "Ticker is required"}), 400
        
        # Get parameters with defaults
        terminal_growth = data.get("terminalGrowth", get_default_terminal_growth())
        risk_free_rate = data.get("riskFreeRate", get_default_risk_free_rate())
        market_return = data.get("marketReturn", get_default_market_return())
        revenue_growth = data.get("revenueGrowth", 0.10)
        
        # Fetch data
        provider = DataProvider(ticker)
        
        current_price = provider.get_current_price()
        shares = provider.get_shares_outstanding()
        beta = provider.get_beta()
        revenue = provider.get_latest_revenue()
        ebit = provider.get_latest_ebit()
        tax_rate = provider.get_tax_rate()
        total_debt = provider.get_total_debt()
        cash = provider.get_cash()
        capex = provider.get_capex()
        depreciation = provider.get_depreciation()
        market_cap = provider.get_market_cap()
        
        # Validate
        if not all([current_price, shares, revenue, ebit]):
            return jsonify({"error": "Insufficient data for this ticker"}), 400
        
        # Calculate metrics
        ebit_margin = ebit / revenue
        reinvestment_rate = estimate_reinvestment_rate(capex, depreciation, revenue)
        
        net_debt = total_debt - cash if total_debt else 0
        enterprise_value = market_cap + net_debt if market_cap else None
        
        if enterprise_value and enterprise_value > 0:
            equity_weight = market_cap / enterprise_value
            debt_weight = net_debt / enterprise_value if net_debt > 0 else 0
        else:
            equity_weight = 1.0
            debt_weight = 0.0
        
        cost_of_equity = calculate_cost_of_equity(risk_free_rate, beta, market_return)
        cost_of_debt = 0.05
        
        wacc_rate = equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)
        
        # Run DCF
        result = dcf_valuation(
            base_revenue=revenue,
            revenue_growth=revenue_growth,
            ebit_margin=ebit_margin,
            tax_rate=tax_rate,
            reinvestment_rate=reinvestment_rate,
            wacc_rate=wacc_rate,
            terminal_growth=terminal_growth,
            shares_outstanding=shares,
        )
        
        intrinsic_value = result["price_per_share"]
        mos = margin_of_safety(intrinsic_value, current_price)
        
        # Find implied growth
        implied_growth = find_implied_growth(
            target_price=current_price,
            base_revenue=revenue,
            ebit_margin=ebit_margin,
            tax_rate=tax_rate,
            reinvestment_rate=reinvestment_rate,
            wacc_rate=wacc_rate,
            terminal_growth=terminal_growth,
            shares_outstanding=shares,
        )
        
        return jsonify({
            "ticker": ticker,
            "currentPrice": current_price,
            "intrinsicValue": intrinsic_value,
            "marginOfSafety": mos,
            "impliedGrowth": implied_growth,
            "inputs": {
                "revenue": revenue,
                "ebitMargin": ebit_margin,
                "taxRate": tax_rate,
                "reinvestmentRate": reinvestment_rate,
                "revenueGrowth": revenue_growth,
                "terminalGrowth": terminal_growth,
                "wacc": wacc_rate,
                "costOfEquity": cost_of_equity,
                "costOfDebt": cost_of_debt,
                "equityWeight": equity_weight,
                "debtWeight": debt_weight,
                "beta": beta,
            },
            "dcf": {
                "pvFcf": result["pv_fcf"],
                "pvTerminalValue": result["pv_terminal_value"],
                "enterpriseValue": result["enterprise_value"],
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
