import numpy as np
import random
from dataclasses import dataclass
from enum import Enum
from typing import List

class DistributionType(Enum):
    RANDOM = "random"
    SORTED = "sorted"
    REVERSE_SORTED = "reverse_sorted"
    NEARLY_SORTED = "nearly_sorted"
    FEW_UNIQUE = "few_unique"

@dataclass
class DatasetConfig:
    size: int
    distribution: DistributionType
    seed: int = 42
    range_min: int = 0
    range_max: int = 1000000

class DatasetGenerator:
    """Generates numerical datasets for algorithm benchmarking."""

    @staticmethod
    def generate(config: DatasetConfig) -> List[int]:
        """Generates a dataset based on the provided configuration."""
        
        np.random.seed(config.seed)
        random.seed(config.seed)
        
        if config.distribution == DistributionType.RANDOM:
            return np.random.randint(config.range_min, config.range_max, config.size).tolist()
            
        elif config.distribution == DistributionType.SORTED:
            return np.arange(config.range_min, config.range_min + config.size).tolist()
            
        elif config.distribution == DistributionType.REVERSE_SORTED:
            return np.arange(config.range_min + config.size, config.range_min, -1).tolist()
            
        elif config.distribution == DistributionType.NEARLY_SORTED:
            arr = np.arange(config.range_min, config.range_min + config.size)
            # Swap approx 5% of elements
            num_swaps = max(1, int(config.size * 0.05))
            for _ in range(num_swaps):
                i, j = np.random.randint(0, config.size, 2)
                arr[i], arr[j] = arr[j], arr[i]
            return arr.tolist()
            
        elif config.distribution == DistributionType.FEW_UNIQUE:
            # Generate only 10% unique values
            unique_count = max(1, int(config.size * 0.1))
            choices = np.random.randint(config.range_min, config.range_max, unique_count)
            return np.random.choice(choices, config.size).tolist()
            
        else:
            raise ValueError(f"Unsupported distribution type: {config.distribution}")
