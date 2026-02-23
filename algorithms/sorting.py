import math
from typing import List
from .base import SortingAlgorithm

class BubbleSort(SortingAlgorithm):
    @property
    def name(self) -> str:
        return "Bubble Sort"
    
    @property
    def time_complexity(self) -> str:
        return "O(n^2)"

    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
            if not swapped:
                break
        return arr

class InsertionSort(SortingAlgorithm):
    @property
    def name(self) -> str:
        return "Insertion Sort"

    @property
    def time_complexity(self) -> str:
        return "O(n^2)"

    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and key < arr[j]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

class MergeSort(SortingAlgorithm):
    @property
    def name(self) -> str:
        return "Merge Sort"

    @property
    def time_complexity(self) -> str:
        return "O(n log n)"

    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class QuickSort(SortingAlgorithm):
    @property
    def name(self) -> str:
        return "Quick Sort"

    @property
    def time_complexity(self) -> str:
        return "O(n log n)"

    def sort(self, data: List[int]) -> List[int]:
        # Utilizing standard Python list comprehension for specific QuickSort implementation clarity
        # Note: This is a recursive implementation suitable for benchmarking, though iteration limit exists
        if len(data) <= 1:
            return data
        else:
            pivot = data[len(data) // 2]
            left = [x for x in data if x < pivot]
            middle = [x for x in data if x == pivot]
            right = [x for x in data if x > pivot]
            return self.sort(left) + middle + self.sort(right)

class HeapSort(SortingAlgorithm):
    @property
    def name(self) -> str:
        return "Heap Sort"

    @property
    def time_complexity(self) -> str:
        return "O(n log n)"

    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)

        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)

        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]
            self._heapify(arr, i, 0)
        
        return arr

    def _heapify(self, arr: List[int], n: int, i: int):
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n and arr[l] > arr[largest]:
            largest = l

        if r < n and arr[r] > arr[largest]:
            largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest)

class TimSort(SortingAlgorithm):
    @property
    def name(self) -> str:
        return "TimSort (Python Native)"

    @property
    def time_complexity(self) -> str:
        return "O(n log n)"

    def sort(self, data: List[int]) -> List[int]:
        # Python's sorted() uses Timsort
        return sorted(data)
