"""Tests for DCF valuation engine."""
import numpy as np
from stock_valuation.dcf import (
    wacc,
    project_revenue,
    project_free_cash_flow,
    terminal_value,
    present_value,
    dcf_valuation,
    margin_of_safety,
)


def test_wacc():
    result = wacc(
        equity_weight=0.8,
        cost_of_equity=0.10,
        debt_weight=0.2,
        cost_of_debt=0.05,
        tax_rate=0.25,
    )
    assert np.isclose(result, 0.8 * 0.10 + 0.2 * 0.05 * 0.75)


def test_project_revenue():
    base = 1000
    growth = 0.10
    result = project_revenue(base, growth, years=3)
    expected = np.array([1100, 1210, 1331])
    assert np.allclose(result, expected)


def test_project_free_cash_flow():
    revenue = np.array([1000, 1100, 1210])
    fcf = project_free_cash_flow(
        revenue, ebit_margin=0.25, tax_rate=0.25, reinvestment_rate=0.30
    )
    # EBIT = 250, 275, 302.5
    # EBIAT = 187.5, 206.25, 226.875
    # FCF = 131.25, 144.375, 158.8125
    expected = np.array([131.25, 144.375, 158.8125])
    assert np.allclose(fcf, expected)


def test_terminal_value():
    tv = terminal_value(final_fcf=100, wacc_rate=0.10, terminal_growth=0.02)
    expected = 100 * 1.02 / (0.10 - 0.02)
    assert np.isclose(tv, expected)


def test_present_value():
    cash_flows = np.array([100, 110, 121])
    pv = present_value(cash_flows, discount_rate=0.10)
    expected = 100 / 1.10 + 110 / 1.10**2 + 121 / 1.10**3
    assert np.isclose(pv, expected)


def test_dcf_valuation():
    result = dcf_valuation(
        base_revenue=10000,
        revenue_growth=0.10,
        ebit_margin=0.20,
        tax_rate=0.25,
        reinvestment_rate=0.30,
        wacc_rate=0.10,
        terminal_growth=0.02,
        shares_outstanding=1000,
        years=5,
    )
    assert "price_per_share" in result
    assert result["price_per_share"] > 0
    assert "enterprise_value" in result


def test_margin_of_safety():
    mos = margin_of_safety(intrinsic_value=100, current_price=80)
    assert np.isclose(mos, 0.20)
    
    mos_negative = margin_of_safety(intrinsic_value=100, current_price=120)
    assert np.isclose(mos_negative, -0.20)
