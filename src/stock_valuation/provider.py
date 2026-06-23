"""Data provider for fetching market and financial data."""
import yfinance as yf


class DataProvider:
    """Fetch financial data for a ticker using yfinance."""
    
    def __init__(self, ticker):
        self.ticker = ticker
        self.stock = yf.Ticker(ticker)
        self._info = None
        self._financials = None
        self._balance_sheet = None
        self._cashflow = None
    
    @property
    def info(self):
        if self._info is None:
            self._info = self.stock.info
        return self._info
    
    @property
    def financials(self):
        if self._financials is None:
            self._financials = self.stock.financials
        return self._financials
    
    @property
    def balance_sheet(self):
        if self._balance_sheet is None:
            self._balance_sheet = self.stock.balance_sheet
        return self._balance_sheet
    
    @property
    def cashflow(self):
        if self._cashflow is None:
            self._cashflow = self.stock.cashflow
        return self._cashflow
    
    def get_current_price(self):
        """Get current stock price."""
        return self.info.get("currentPrice") or self.info.get("regularMarketPrice")
    
    def get_shares_outstanding(self):
        """Get shares outstanding."""
        return self.info.get("sharesOutstanding")
    
    def get_beta(self):
        """Get beta for cost of equity calculation."""
        return self.info.get("beta", 1.0)
    
    def get_market_cap(self):
        """Get market capitalization."""
        return self.info.get("marketCap")
    
    def get_latest_revenue(self):
        """Get most recent annual revenue."""
        if self.financials is not None and not self.financials.empty:
            rev = self.financials.loc["Total Revenue"].iloc[0] if "Total Revenue" in self.financials.index else None
            return rev
        return None
    
    def get_latest_ebit(self):
        """Get most recent EBIT."""
        if self.financials is not None and not self.financials.empty:
            ebit = self.financials.loc["EBIT"].iloc[0] if "EBIT" in self.financials.index else None
            return ebit
        return None
    
    def get_tax_rate(self):
        """Calculate effective tax rate from financials."""
        if self.financials is not None and not self.financials.empty:
            try:
                pretax_income = self.financials.loc["Pretax Income"].iloc[0] if "Pretax Income" in self.financials.index else None
                tax_provision = self.financials.loc["Tax Provision"].iloc[0] if "Tax Provision" in self.financials.index else None
                if pretax_income and tax_provision and pretax_income > 0:
                    return tax_provision / pretax_income
            except:
                pass
        return 0.25  # Default corporate tax rate
    
    def get_total_debt(self):
        """Get total debt from balance sheet."""
        if self.balance_sheet is not None and not self.balance_sheet.empty:
            debt = self.balance_sheet.loc["Total Debt"].iloc[0] if "Total Debt" in self.balance_sheet.index else None
            return debt
        return 0
    
    def get_cash(self):
        """Get cash and equivalents."""
        if self.balance_sheet is not None and not self.balance_sheet.empty:
            cash = self.balance_sheet.loc["Cash And Cash Equivalents"].iloc[0] if "Cash And Cash Equivalents" in self.balance_sheet.index else None
            return cash if cash else 0
        return 0
    
    def get_capex(self):
        """Get capital expenditures."""
        if self.cashflow is not None and not self.cashflow.empty:
            capex = self.cashflow.loc["Capital Expenditure"].iloc[0] if "Capital Expenditure" in self.cashflow.index else None
            return abs(capex) if capex else None
        return None
    
    def get_depreciation(self):
        """Get depreciation and amortization."""
        if self.cashflow is not None and not self.cashflow.empty:
            dep = self.cashflow.loc["Depreciation And Amortization"].iloc[0] if "Depreciation And Amortization" in self.cashflow.index else None
            return dep if dep else None
        return None
