from models import EnergyStats
import statistics
from typing import List


def simple_linear_regression(x: List[float], y: List[float]) -> float:
    """
    Calculate slope of linear regression without scipy/numpy.
    Uses the formula: slope = Σ((x - x̄)(y - ȳ)) / Σ((x - x̄)²)
    """
    n = len(x)
    if n < 2:
        return 0.0
    
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    
    numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def calculations(energy_levels: List[int]) -> EnergyStats:
    """
    Calculate statistics for energy levels without heavy dependencies.
    """
    if len(energy_levels) < 1:
        raise ValueError("Need at least one energy level")
    
    # Edge case: single value
    if len(energy_levels) == 1:
        return EnergyStats(
            mean=energy_levels[0],
            median=energy_levels[0],
            min=energy_levels[0],
            max=energy_levels[0],
            std_dev=0.0,
            trend_slope=0.0
        )
    
    # Calculate trend slope
    x = list(range(len(energy_levels)))  # [0, 1, 2, 3, 4, 5, 6]
    slope = simple_linear_regression(x, energy_levels)
    
    # Standard deviation
    std_dev = statistics.stdev(energy_levels)
    
    return EnergyStats(
        mean=statistics.mean(energy_levels),
        median=statistics.median(energy_levels),
        min=min(energy_levels),
        max=max(energy_levels),
        std_dev=std_dev,
        trend_slope=slope
    )