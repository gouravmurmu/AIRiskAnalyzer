# src/config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    """Central configuration for the AI Risk Analyzer."""
    
    # Data Settings
    START_DATE: str = "2020-01-01"
    END_DATE: str = "2024-01-01"
    DEFAULT_TICKERS = ["AAPL", "MSFT", "BTC-USD", "ETH-USD"]
    
    # Analysis Settings
    RISK_FREE_RATE: float = 0.04  # 4% annual risk-free rate
    TRADING_DAYS_STOCK: int = 252
    TRADING_DAYS_CRYPTO: int = 365
    
    # Monte Carlo Settings
    MC_SIMULATIONS: int = 1000
    MC_TIME_HORIZON: int = 252  # 1 year
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, 'data', 'raw')
    REPORTS_DIR: str = os.path.join(BASE_DIR, 'reports')
    
    # Plotting
    PLOT_STYLE: str = 'seaborn-v0_8-darkgrid'
