import math
from typing import List
from .base import SearchingAlgorithm

class LinearSearch(SearchingAlgorithm):
    @property
    def name(self) -> str:
        return "Linear Search"

    @property
    def time_complexity(self) -> str:
        return "O(n)"

    def search(self, data: List[int], target: int) -> int:
        for i, val in enumerate(data):
            if val == target:
                return i
        return -1

class BinarySearch(SearchingAlgorithm):
    @property
    def name(self) -> str:
        return "Binary Search"

    @property
    def time_complexity(self) -> str:
        return "O(log n)"

    def search(self, data: List[int], target: int) -> int:
        # Assumes data is sorted
        low = 0
        high = len(data) - 1
        mid = 0

        while low <= high:
            mid = (high + low) // 2
            if data[mid] < target:
                low = mid + 1
            elif data[mid] > target:
                high = mid - 1
            else:
                return mid
        return -1

class JumpSearch(SearchingAlgorithm):
    @property
    def name(self) -> str:
        return "Jump Search"

    @property
    def time_complexity(self) -> str:
        return "O(sqrt(n))"

    def search(self, data: List[int], target: int) -> int:
        # Assumes data is sorted
        n = len(data)
        if n == 0:
            return -1
            
        step = int(math.sqrt(n))
        prev = 0
        
        while prev < n and data[min(step, n) - 1] < target:
            prev = step
            step += int(math.sqrt(n))
            if prev >= n:
                return -1
        
        while prev < min(step, n):
            if data[prev] == target:
                return prev
            prev += 1
            
        return -1
