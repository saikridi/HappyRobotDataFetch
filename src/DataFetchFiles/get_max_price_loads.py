from fastapi import HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd


class LoadSelectionResponse(BaseModel):
    selected_loads: List[Dict[str, Any]]
    total_amount: float
    total_weight: int
    total_loads: int

def knapsack_01(loads_df: pd.DataFrame, max_weight: int) -> LoadSelectionResponse:
    # Data Preparation
    n = len(loads_df)
    weights = loads_df['weights'].tolist()
    profits = loads_df['loadboard_rate'].tolist()
    
    # Create DP table: dp[i][w] = maximum profit with first i items and weight w
    dp = [[0 for _ in range(max_weight + 1)] for _ in range(n + 1)]
    
    # Fill DP table
    for i in range(1, n + 1):
        for w in range(max_weight + 1):
            dp[i][w] = dp[i-1][w]
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + profits[i-1])
    
    # Back Tracking
    selected_indices = []
    w = max_weight
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected_indices.append(i-1)
            w -= weights[i-1]
    
    # Get selected loads
    selected_loads = []
    total_weight = 0
    total_amount = 0.0
    
    for idx in selected_indices:
        load_data = loads_df.iloc[idx].to_dict()
        selected_loads.append(load_data)
        total_weight += weights[idx]
        total_amount += profits[idx]
    
    
    return LoadSelectionResponse(
        selected_loads=selected_loads,
        total_amount=total_amount,
        total_weight=total_weight,
        total_loads=len(selected_loads)
    )
    

def get_optimal_loads(max_load_weight: int, df: pd.DataFrame) -> LoadSelectionResponse:
    result = knapsack_01(df, max_load_weight)
    return result
