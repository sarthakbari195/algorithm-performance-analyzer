"""
Quick validation test for the Algorithm Performance Analyzer
"""
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from algorithms.sorting import BubbleSort, QuickSort, MergeSort, HeapSort
        from algorithms.searching import LinearSearch, BinarySearch
        from core.benchmark_engine import BenchmarkEngine
        from core.dataset_generator import DatasetGenerator, DistributionType
        from core.complexity_validator import ComplexityValidator
        from visualization.plotter import Plotter
        print("✓ All imports successful")
        return True
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_algorithm_execution():
    """Test that algorithms execute correctly"""
    print("\nTesting algorithm execution...")
    
    try:
        from algorithms.sorting import QuickSort
        
        algo = QuickSort()
        test_data = [5, 2, 8, 1, 9]
        result = algo.sort(test_data)
        
        assert result == [1, 2, 5, 8, 9], f"Expected [1, 2, 5, 8, 9], got {result}"
        print(f"✓ QuickSort works: {test_data} → {result}")
        return True
    except Exception as e:
        print(f"✗ Algorithm execution error: {e}")
        return False

def test_dataset_generation():
    """Test dataset generation"""
    print("\nTesting dataset generation...")
    
    try:
        from core.dataset_generator import DatasetGenerator, DatasetConfig, DistributionType
        
        config = DatasetConfig(size=100, distribution=DistributionType.RANDOM, seed=42)
        data = DatasetGenerator.generate(config)
        
        assert len(data) == 100, f"Expected 100 elements, got {len(data)}"
        print(f"✓ Dataset generation works: Generated {len(data)} elements")
        return True
    except Exception as e:
        print(f"✗ Dataset generation error: {e}")
        return False

def test_benchmark_engine():
    """Test benchmark engine"""
    print("\nTesting benchmark engine...")
    
    try:
        from core.benchmark_engine import BenchmarkEngine
        from algorithms.sorting import QuickSort
        from core.dataset_generator import DistributionType
        
        engine = BenchmarkEngine()
        results = engine.benchmark_algorithm(
            QuickSort, 
            sizes=[100, 200], 
            trials=2,
            distribution=DistributionType.RANDOM
        )
        
        assert len(results) == 2, f"Expected 2 results, got {len(results)}"
        print(f"✓ Benchmark engine works: Ran {len(results)} benchmarks")
        return True
    except Exception as e:
        print(f"✗ Benchmark engine error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Algorithm Performance Analyzer - Validation Test")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_algorithm_execution,
        test_dataset_generation,
        test_benchmark_engine
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✓ All systems operational!")
        return 0
    else:
        print("\n✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
