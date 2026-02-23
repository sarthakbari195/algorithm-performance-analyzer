from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Any, Union, Protocol
import random

T = TypeVar('T', bound=int)

class Algorithm(ABC):
    """
    Abstract base class for all algorithms.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Category of the algorithm e.g., 'Sorting', 'Searching'"""
        pass

    @property
    @abstractmethod
    def time_complexity(self) -> str:
        """Expected theoretical time complexity (e.g., 'O(n log n)')"""
        pass

class SortingAlgorithm(Algorithm):
    """Base class for sorting algorithms."""
    
    @property
    def category(self) -> str:
        return "Sorting"

    @abstractmethod
    def sort(self, data: List[T]) -> List[T]:
        """
        Sorts the input list.
        MUST RETURN A NEW LIST. DO NOT MUTATE INPUT IN PLACE unless copying first.
        """
        pass

class SearchingAlgorithm(Algorithm):
    """Base class for searching algorithms."""

    @property
    def category(self) -> str:
        return "Searching"

    @abstractmethod
    def search(self, data: List[T], target: T) -> int:
        """
        Searches for target in data.
        Returns index if found, else -1.
        Data is assumed to be sorted for Binary/Jump search.
        """
        pass
