import sys
import os
import argparse
import logging
from typing import List, Type

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.base import Algorithm
from algorithms.sorting import BubbleSort, InsertionSort, MergeSort, QuickSort, HeapSort, TimSort
from algorithms.searching import LinearSearch, BinarySearch, JumpSearch
from core.benchmark_engine import BenchmarkEngine
from core.dataset_generator import DistributionType
from core.complexity_validator import ComplexityValidator
from visualization.report_generator import ReportGenerator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ALGO_REGISTRY = {
    'bubble_sort': BubbleSort,
    'insertion_sort': InsertionSort,
    'merge_sort': MergeSort,
    'quick_sort': QuickSort,
    'heap_sort': HeapSort,
    'timsort': TimSort,
    'linear_search': LinearSearch,
    'binary_search': BinarySearch,
    'jump_search': JumpSearch
}

SORTING_ALGOS = [BubbleSort, InsertionSort, MergeSort, QuickSort, HeapSort, TimSort]
SEARCHING_ALGOS = [LinearSearch, BinarySearch, JumpSearch]

def get_algorithm_class(name: str) -> Type[Algorithm]:
    return ALGO_REGISTRY.get(name.lower())

def main():
    parser = argparse.ArgumentParser(description="Algorithm Performance Analyzer")
    
    parser.add_argument('--algorithm', type=str, help='Specific algorithm to run (e.g., quick_sort)')
    parser.add_argument('--mode', type=str, choices=['single', 'compare', 'all_sorting', 'all_searching'], default='compare', help='Benchmarking mode')
    parser.add_argument('--dataset', type=str, choices=[d.value for d in DistributionType], default='random', help='Data distribution')
    parser.add_argument('--size', type=int, default=10000, dest='max_size', help='Maximum input size (default: 10000)') # Maps to max_size internally
    parser.add_argument('--steps', type=int, default=5, help='Number of size steps')
    parser.add_argument('--trials', type=int, default=5, help='Number of trials per size')
    parser.add_argument('--validate-complexity', action='store_true', help='Perform empirical complexity validation')
    
    args = parser.parse_args()
    
    # Generate size range
    step_size = args.max_size // args.steps
    sizes = [step_size * i for i in range(1, args.steps + 1)]
    
    # Handle edge case where steps > max_size (unlikely default, but possible user input)
    sizes = [s for s in sizes if s > 0]
    if not sizes:
        sizes = [args.max_size]

    distribution = DistributionType(args.dataset)
    
    engine = BenchmarkEngine()
    
    target_algos = []
    
    if args.algorithm:
        algo_cls = get_algorithm_class(args.algorithm)
        if not algo_cls:
            logger.error(f"Algorithm {args.algorithm} not found.")
            return
        target_algos = [algo_cls]
    elif args.mode == 'all_sorting':
        target_algos = SORTING_ALGOS
    elif args.mode == 'all_searching':
        target_algos = SEARCHING_ALGOS
    elif args.mode == 'compare':
        # Default comparison if nothing specific
        logger.info("Comparing all sorting algorithms by default.")
        target_algos = SORTING_ALGOS
        
    logger.info(f"Starting {args.mode} benchmark on {len(target_algos)} algorithms...")
    logger.info(f"Input sizes: {sizes}")
    
    results_df = engine.compare_algorithms(target_algos, sizes, args.trials, distribution)
    
    complexity_df = None
    if args.validate_complexity:
        logger.info("Validating complexity...")
        complexity_df = ComplexityValidator.validate(results_df)
        print("\nComplexity Validation Results:")
        print(complexity_df.to_string())
        
    # Generate Report
    try:
        reporter = ReportGenerator()
        report_path = reporter.generate_report(results_df, complexity_df)
        logger.info(f"Report generated at {report_path}")
    except Exception as e:
        logger.error(f"Failed to generate visualization report: {e}")
    
    engine.save_results()
    logger.info("Benchmark complete.")

if __name__ == "__main__":
    main()
