from dataclasses import dataclass, field
from typing import List, Optional
import numpy as np

@dataclass
class TrialResult:
    """Raw data from a single execution trial."""
    algorithm_name: str
    input_size: int
    execution_time: float  # seconds
    peak_memory: int       # bytes
    distribution: str
    timestamp: float

@dataclass
class BenchmarkMetrics:
    """Aggregated metrics for an algorithm run over multiple trials."""
    algorithm_name: str
    input_size: int
    distribution: str
    num_trials: int
    
    # Time metrics (Seconds)
    mean_time: float
    median_time: float
    std_dev_time: float
    min_time: float
    max_time: float
    
    # Memory metrics (Bytes)
    mean_memory: float
    peak_memory: int
    
    # Theoretical Complexity
    complexity_class: str = "Unknown"
    
    def to_dict(self):
        return {
            "Algorithm": self.algorithm_name,
            "Input Size": self.input_size,
            "Distribution": self.distribution,
            "Trials": self.num_trials,
            "Mean Time (s)": self.mean_time,
            "Median Time (s)": self.median_time,
            "Std Dev Time": self.std_dev_time,
            "Mean Memory (B)": self.mean_memory,
            "Peak Memory (B)": self.peak_memory,
            "Complexity": self.complexity_class
        }

class MetricCalculator:
    """Helper to compute statistics from raw trial data."""
    
    @staticmethod
    def calculate(algorithm_name: str, input_size: int, distribution: str, trials: List[TrialResult]) -> BenchmarkMetrics:
        times = [t.execution_time for t in trials]
        memories = [t.peak_memory for t in trials]
        
        return BenchmarkMetrics(
            algorithm_name=algorithm_name,
            input_size=input_size,
            distribution=distribution,
            num_trials=len(trials),
            mean_time=float(np.mean(times)),
            median_time=float(np.median(times)),
            std_dev_time=float(np.std(times)),
            min_time=float(np.min(times)),
            max_time=float(np.max(times)),
            mean_memory=float(np.mean(memories)),
            peak_memory=int(np.max(memories)),
            complexity_class="" # Filled later by validator
        )
