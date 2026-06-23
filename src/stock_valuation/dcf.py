"""DCF valuation calculation engine."""
import numpy as np


def wacc(equity_weight, cost_of_equity, debt_weight, cost_of_debt, tax_rate):
    """Calculate weighted average cost of capital."""
    return equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)


def project_revenue(base_revenue, growth_rate, years=5):
    """Project revenue growth over N years."""
    return base_revenue * (1 + growth_rate) ** np.arange(1, years + 1)


def project_free_cash_flow(revenue, ebit_margin, tax_rate, reinvestment_rate):
    """Calculate FCF from revenue projections."""
    ebit = revenue * ebit_margin
    ebiat = ebit * (1 - tax_rate)
    fcf = ebiat * (1 - reinvestment_rate)
    return fcf


def terminal_value(final_fcf, wacc_rate, terminal_growth):
    """Calculate terminal value using perpetuity growth model."""
    return final_fcf * (1 + terminal_growth) / (wacc_rate - terminal_growth)


def present_value(cash_flows, discount_rate):
    """Discount cash flows to present value."""
    periods = np.arange(1, len(cash_flows) + 1)
    return np.sum(cash_flows / (1 + discount_rate) ** periods)


def dcf_valuation(
    base_revenue,
    revenue_growth,
    ebit_margin,
    tax_rate,
    reinvestment_rate,
    wacc_rate,
    terminal_growth,
    shares_outstanding,
    years=5,
):
    """
    Complete DCF valuation returning price per share.
    
    Returns:
        dict with keys: fcf, terminal_value, enterprise_value, price_per_share
    """
    revenues = project_revenue(base_revenue, revenue_growth, years)
    fcf = project_free_cash_flow(revenues, ebit_margin, tax_rate, reinvestment_rate)
    
    pv_fcf = present_value(fcf, wacc_rate)
    tv = terminal_value(fcf[-1], wacc_rate, terminal_growth)
    pv_tv = tv / (1 + wacc_rate) ** years
    
    enterprise_value = pv_fcf + pv_tv
    price_per_share = enterprise_value / shares_outstanding
    
    return {
        "fcf": fcf,
        "pv_fcf": pv_fcf,
        "terminal_value": tv,
        "pv_terminal_value": pv_tv,
        "enterprise_value": enterprise_value,
        "price_per_share": price_per_share,
    }


def margin_of_safety(intrinsic_value, current_price):
    """Calculate margin of safety as percentage."""
    return (intrinsic_value - current_price) / intrinsic_value


def find_implied_growth(
    target_price,
    base_revenue,
    ebit_margin,
    tax_rate,
    reinvestment_rate,
    wacc_rate,
    terminal_growth,
    shares_outstanding,
    years=5,
    max_iter=50,
    tol=0.01,
):
    """
    Find the revenue growth rate that results in target price using bisection.
    
    Returns:
        growth_rate or None if not found
    """
    low, high = -0.50, 1.0  # Search range: -50% to 100% growth
    
    for _ in range(max_iter):
        mid = (low + high) / 2.0
        
        result = dcf_valuation(
            base_revenue,
            mid,
            ebit_margin,
            tax_rate,
            reinvestment_rate,
            wacc_rate,
            terminal_growth,
            shares_outstanding,
            years,
        )
        
        diff = result["price_per_share"] - target_price
        
        if abs(diff) < tol:
            return mid
        
        if diff < 0:
            low = mid
        else:
            high = mid
    
    return None  # Did not converge
