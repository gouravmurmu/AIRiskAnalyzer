# src/risk_metrics.py
import numpy as np
import pandas as pd
from typing import Dict, Union

def calculate_metrics(returns: pd.DataFrame, risk_free_rate: float = 0.04) -> pd.DataFrame:
    """
    Computes key risk metrics for each asset in the returns DataFrame.
    
    Args:
        returns (pd.DataFrame): Daily returns for assets.
        risk_free_rate (float): Annualized risk-free rate (decimal, e.g., 0.04).
        
    Returns:
        pd.DataFrame: A DataFrame with metrics as rows and assets as columns.
    """
    metrics = {}
    
    # Assuming daily returns, annualized factor is 252 (trading days)
    # For crypto it might be 365, but we'll stick to a standard conversion for comparison or make it configurable.
    # We'll use 252 for consistency with standard financial reporting unless specified.
    ANNUALIZATION_FACTOR = 252
    
    for ticker in returns.columns:
        asset_ret = returns[ticker]
        
        # 1. Total Cumulative Return
        total_return = (1 + asset_ret).prod() - 1
        
        # 2. Annualized Volatility
        volatility = asset_ret.std() * np.sqrt(ANNUALIZATION_FACTOR)
        
        # 3. Sharpe Ratio
        # Excess daily returns
        daily_rf = (1 + risk_free_rate) ** (1/ANNUALIZATION_FACTOR) - 1
        excess_ret = asset_ret - daily_rf
        sharpe_ratio = (excess_ret.mean() / asset_ret.std()) * np.sqrt(ANNUALIZATION_FACTOR)
        
        # 4. Max Drawdown
        cumulative = (1 + asset_ret).cumprod()
        peak = cumulative.cummax()
        drawdown = (cumulative - peak) / peak
        max_drawdown = drawdown.min()
        
        # 5. Value at Risk (VaR) - 95% Confidence
        sorted_returns = np.sort(asset_ret)
        index_95 = int((1 - 0.95) * len(sorted_returns))
        var_95 = sorted_returns[index_95]
        
        # 6. Conditional VaR (CVaR) - 95%
        cvar_95 = sorted_returns[:index_95].mean()
        
        metrics[ticker] = {
            'Total Return': total_return,
            'Annualized Volatility': volatility,
            'Sharpe Ratio': sharpe_ratio,
            'Max Drawdown': max_drawdown,
            'VaR (95%)': var_95,
            'CVaR (95%)': cvar_95
        }
        
    return pd.DataFrame(metrics)

if __name__ == "__main__":
    # Test
    dates = pd.date_range(start="2023-01-01", periods=100)
    data = np.random.normal(0.001, 0.02, (100, 2))
    df = pd.DataFrame(data, index=dates, columns=['Asset A', 'Asset B'])
    
    results = calculate_metrics(df)
    print("Risk Metrics:\n", results)
