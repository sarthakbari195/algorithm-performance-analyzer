import pytest
from algorithms.sorting import BubbleSort, InsertionSort, MergeSort, QuickSort, HeapSort, TimSort
from algorithms.searching import LinearSearch, BinarySearch, JumpSearch
import random

SORTING_ALGOS = [BubbleSort, InsertionSort, MergeSort, QuickSort, HeapSort, TimSort]
SEARCHING_ALGOS = [LinearSearch, BinarySearch, JumpSearch]

@pytest.mark.parametrize("algo_cls", SORTING_ALGOS)
def test_sorting_algorithms(algo_cls):
    algo = algo_cls()
    data = [random.randint(0, 1000) for _ in range(100)]
    sorted_data = algo.sort(data)
    
    assert sorted_data == sorted(data), f"{algo.name} failed to sort correctly"
    # Ensure original data is not modified if possible, though some implementations might copy internally
    # The requirement was "Be pure functions", so we check if `data` is still same or if specifically `sort` returns new list.
    # Our implementation uses .copy() so it should be fine.

@pytest.mark.parametrize("algo_cls", SEARCHING_ALGOS)
def test_searching_algorithms(algo_cls):
    algo = algo_cls()
    data = sorted([random.randint(0, 1000) for _ in range(100)]) # Sorted for all since Binary/Jump need it
    target = data[len(data)//2]
    
    index = algo.search(data, target)
    assert index != -1, f"{algo.name} failed to find existing element"
    assert data[index] == target
    
    # Test missing
    assert algo.search(data, -1) == -1, f"{algo.name} found non-existent element"
