import time
import tracemalloc
import logging
import os
import gc
import pandas as pd
from typing import List, Dict, Type, Any
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from tqdm import tqdm

from algorithms.base import Algorithm, SortingAlgorithm, SearchingAlgorithm
from .dataset_generator import DatasetGenerator, DatasetConfig, DistributionType
from .metrics import TrialResult, BenchmarkMetrics, MetricCalculator

logger = logging.getLogger(__name__)

class BenchmarkEngine:
    """Core engine for running algorithm benchmarks."""

    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        self.results: List[BenchmarkMetrics] = []

    def _run_single_trial(self, algorithm: Algorithm, data: List[int], track_memory: bool = True, **kwargs) -> TrialResult:
        """
        Runs a single trial of the algorithm.
        
        Args:
            algorithm: The algorithm instance to run.
            data: The input data.
            track_memory: Whether to track memory usage (adds overhead).
            **kwargs: Additional arguments for the algorithm (e.g., target for search).
        
        Returns:
            TrialResult: The result of the trial.
        """
        # Garbage collection before run to minimize interference
        gc.collect()
        
        # Start memory tracking if requested
        if track_memory:
            tracemalloc.start()
        
        start_time = time.perf_counter()
        
        # Execute
        if isinstance(algorithm, SortingAlgorithm):
            algorithm.sort(data) 
        elif isinstance(algorithm, SearchingAlgorithm):
            target = kwargs.get('target', data[0] if data else 0)
            algorithm.search(data, target)
            
        end_time = time.perf_counter()
        
        peak_memory = 0
        if track_memory:
            _, peak_memory = tracemalloc.get_traced_memory()
            tracemalloc.stop()
        
        return TrialResult(
            algorithm_name=algorithm.name,
            input_size=len(data),
            execution_time=end_time - start_time,
            peak_memory=peak_memory,
            distribution="N/A", # Set by caller
            timestamp=time.time()
        )

    def benchmark_algorithm(self, 
                          algorithm_class: Type[Algorithm], 
                          sizes: List[int], 
                          trials: int = 5,
                          distribution: DistributionType = DistributionType.RANDOM,
                          seed: int = 42,
                          track_memory: bool = True) -> List[BenchmarkMetrics]:
        """
        Benchmarks a specific algorithm across multiple input sizes.
        """
        algorithm = algorithm_class()
        logger.info(f"Benchmarking {algorithm.name} with sizes {sizes}, trials={trials}, track_memory={track_memory}")
        
        algo_metrics = []

        for size in tqdm(sizes, desc=f"Benchmarking {algorithm.name}"):
            trial_results = []
            
            # Generate dataset
            config = DatasetConfig(size=size, distribution=distribution, seed=seed)
            # data generation is outside timing
            base_data = DatasetGenerator.generate(config)
            
            # For searching, we might need sorted data or a specific target
            # If searching algorithm, ensure data is sorted if required (Binary/Jump)
            # But wait, the requirement says "searching" algorithms. 
            # Binary Search requires sorted data. 
            # If we pass random data to Binary Search, it fails.
            # We should probably pre-sort the data for searching algorithms if strictly required,
            # or handle it in the setup.
            # For fairness, if we benchmark searching, we typically search in a sorted array.
            run_data = base_data
            search_target = 0
            if isinstance(algorithm, SearchingAlgorithm):
                run_data = sorted(base_data)
                # Pick a random target from the data to ensure hit, or outside for miss.
                # Let's pick a value that exists for stable benchmarking.
                search_target = run_data[size // 2] if size > 0 else 0

            # Warm-up run (untracked)
            try:
                if isinstance(algorithm, SortingAlgorithm):
                    algorithm.sort(run_data[:100] if len(run_data) > 100 else run_data)
                elif isinstance(algorithm, SearchingAlgorithm):
                    algorithm.search(run_data, search_target)
            except Exception:
                pass # Ignore warmup errors

            for i in range(trials):
                # Copy data for sorting to ensure each trial starts with same state
                # (Sorting algos in this project return new list, but some might mutate if not careful.
                # The base class says "Return sorted list", assumes safety.
                # However, to be safe and measure *just* the sort time of the input, copy is strictly needed if mutation happens.
                # Our algorithms.py uses .copy(), so input is safe.
                # But passing a large list by reference is cheap.
                
                trial_input = run_data
                
                result = self._run_single_trial(algorithm, trial_input, track_memory=track_memory, target=search_target)
                result.distribution = distribution.value
                trial_results.append(result)
            
            # Aggregate metrics
            metrics = MetricCalculator.calculate(algorithm.name, size, distribution.value, trial_results)
            metrics.complexity_class = algorithm.time_complexity # Theoretical
            algo_metrics.append(metrics)
            self.results.append(metrics)
            
        return algo_metrics

    def compare_algorithms(self, 
                         algorithms: List[Type[Algorithm]], 
                         sizes: List[int],
                         trials: int = 5,
                         distribution: DistributionType = DistributionType.RANDOM) -> pd.DataFrame:
        """
        Runs benchmarks for multiple algorithms and returns a consolidated DataFrame.
        """
        all_metrics = []
        for algo_cls in algorithms:
            metrics = self.benchmark_algorithm(algo_cls, sizes, trials, distribution)
            all_metrics.extend(metrics)
            
        return self.get_results_df()

    def get_results_df(self) -> pd.DataFrame:
        """Returns the current results as a pandas DataFrame."""
        return pd.DataFrame([m.to_dict() for m in self.results])

    def save_results(self, filename: str = "benchmark_results.csv"):
        """Saves results to CSV and JSON."""
        df = self.get_results_df()
        
        # Save CSV
        csv_path = os.path.join(self.output_dir, filename)
        df.to_csv(csv_path, index=False)
        logger.info(f"Results saved to {csv_path}")
        
        # Save JSON
        json_filename = filename.replace('.csv', '.json')
        json_path = os.path.join(self.output_dir, json_filename)
        df.to_json(json_path, orient='records', indent=4)
        logger.info(f"Results saved to {json_path}")
