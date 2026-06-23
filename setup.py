"""Setup script for stock_valuation package."""
from setuptools import setup, find_packages

setup(
    name="stock_valuation",
    version="0.1.0",
    description="DCF-based stock valuation CLI",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "yfinance>=0.2.40",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "typer>=0.9.0",
    ],
    extras_require={
        "dev": ["pytest>=7.4.0"],
    },
    entry_points={
        "console_scripts": [
            "stock-valuation=stock_valuation.cli:app",
        ],
    },
    python_requires=">=3.11",
)
