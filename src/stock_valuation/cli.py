"""CLI entrypoint for stock valuation."""
import typer
from stock_valuation.provider import DataProvider
from stock_valuation.dcf import dcf_valuation, margin_of_safety, find_implied_growth
from stock_valuation.utils import (
    get_default_risk_free_rate,
    get_default_market_return,
    get_default_terminal_growth,
    calculate_cost_of_equity,
    estimate_reinvestment_rate,
    format_currency,
    format_percent,
)

app = typer.Typer()


@app.command()
def main(
    ticker: str,
    terminal_growth: float = typer.Option(None, help="Terminal growth rate"),
    risk_free_rate: float = typer.Option(None, help="Risk-free rate"),
    market_return: float = typer.Option(None, help="Market return"),
    revenue_growth: float = typer.Option(0.10, help="Revenue growth assumption"),
):
    """Run DCF valuation for a stock ticker."""
    
    # Set defaults
    if terminal_growth is None:
        terminal_growth = get_default_terminal_growth()
    if risk_free_rate is None:
        risk_free_rate = get_default_risk_free_rate()
    if market_return is None:
        market_return = get_default_market_return()
    
    typer.echo(f"\nFetching data for {ticker}...")
    
    try:
        provider = DataProvider(ticker)
        
        # Fetch required data
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
        
        # Validate critical data
        if not current_price:
            typer.echo("Error: Could not fetch current price", err=True)
            raise typer.Exit(1)
        if not shares:
            typer.echo("Error: Could not fetch shares outstanding", err=True)
            raise typer.Exit(1)
        if not revenue:
            typer.echo("Error: Could not fetch revenue data", err=True)
            raise typer.Exit(1)
        if not ebit:
            typer.echo("Error: Could not fetch EBIT data", err=True)
            raise typer.Exit(1)
        
        # Calculate derived metrics
        ebit_margin = ebit / revenue
        reinvestment_rate = estimate_reinvestment_rate(capex, depreciation, revenue)
        
        # Calculate WACC
        net_debt = total_debt - cash if total_debt else 0
        enterprise_value = market_cap + net_debt if market_cap else None
        
        if enterprise_value and enterprise_value > 0:
            equity_weight = market_cap / enterprise_value
            debt_weight = net_debt / enterprise_value if net_debt > 0 else 0
        else:
            equity_weight = 1.0
            debt_weight = 0.0
        
        cost_of_equity = calculate_cost_of_equity(risk_free_rate, beta, market_return)
        cost_of_debt = 0.05  # Simplified assumption
        
        wacc_rate = (
            equity_weight * cost_of_equity + 
            debt_weight * cost_of_debt * (1 - tax_rate)
        )
        
        # Run DCF valuation
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
        typer.echo("\nCalculating implied growth rate...")
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
        
        # Display results
        typer.echo(f"\n{'='*60}")
        typer.echo(f"DCF VALUATION RESULTS: {ticker}")
        typer.echo(f"{'='*60}\n")
        
        typer.echo("INPUT ASSUMPTIONS:")
        typer.echo(f"  Revenue (TTM):           {format_currency(revenue)}")
        typer.echo(f"  EBIT Margin:             {format_percent(ebit_margin)}")
        typer.echo(f"  Tax Rate:                {format_percent(tax_rate)}")
        typer.echo(f"  Reinvestment Rate:       {format_percent(reinvestment_rate)}")
        typer.echo(f"  Revenue Growth:          {format_percent(revenue_growth)}")
        typer.echo(f"  Terminal Growth:         {format_percent(terminal_growth)}")
        typer.echo(f"  WACC:                    {format_percent(wacc_rate)}")
        typer.echo(f"    - Cost of Equity:      {format_percent(cost_of_equity)}")
        typer.echo(f"    - Cost of Debt:        {format_percent(cost_of_debt)}")
        typer.echo(f"    - Equity Weight:       {format_percent(equity_weight)}")
        typer.echo(f"    - Debt Weight:         {format_percent(debt_weight)}")
        typer.echo(f"  Beta:                    {beta:.2f}")
        
        typer.echo("\nVALUATION OUTPUT:")
        typer.echo(f"  Current Price:           ${current_price:.2f}")
        typer.echo(f"  Intrinsic Value:         ${intrinsic_value:.2f}")
        typer.echo(f"  Margin of Safety:        {format_percent(mos)}")
        
        if mos > 0:
            typer.echo(f"  → Stock is UNDERVALUED by {format_percent(mos)}")
        else:
            typer.echo(f"  → Stock is OVERVALUED by {format_percent(abs(mos))}")
        
        typer.echo("\nIMPLIED GROWTH:")
        if implied_growth is not None:
            typer.echo(f"  Implied Revenue Growth:  {format_percent(implied_growth)}")
            typer.echo(f"  → Market is pricing in {format_percent(implied_growth)} revenue growth")
        else:
            typer.echo("  Could not find implied growth rate (price outside feasible range)")
        
        typer.echo(f"\n{'='*60}\n")
        
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
