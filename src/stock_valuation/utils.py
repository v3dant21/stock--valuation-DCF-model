"""Utility functions for defaults and formatting."""


def get_default_risk_free_rate():
    """Default risk-free rate (10-year treasury)."""
    return 0.04


def get_default_market_return():
    """Default market return."""
    return 0.10


def get_default_terminal_growth():
    """Default terminal growth rate."""
    return 0.025


def calculate_cost_of_equity(risk_free_rate, beta, market_return):
    """Calculate cost of equity using CAPM."""
    return risk_free_rate + beta * (market_return - risk_free_rate)


def estimate_reinvestment_rate(capex, depreciation, revenue):
    """Estimate reinvestment rate from capex and depreciation."""
    if capex and depreciation and revenue:
        net_capex = capex - depreciation
        return net_capex / revenue
    return 0.30  # Default assumption


def format_currency(value):
    """Format value as currency."""
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    else:
        return f"${value:,.0f}"


def format_percent(value):
    """Format value as percentage."""
    return f"{value*100:.2f}%"
