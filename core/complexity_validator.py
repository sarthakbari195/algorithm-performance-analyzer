import numpy as np
import pandas as pd
from typing import List, Dict, Any
from scipy.optimize import curve_fit
import logging

logger = logging.getLogger(__name__)

class ComplexityEstimator:
    """
    Advanced research-grade complexity estimation using data-driven curve fitting.
    """

    @staticmethod
    def _constant_model(n, a):
        return np.full_like(n, a, dtype=float)

    @staticmethod
    def _log_model(n, a, b):
        n_safe = np.maximum(n, 1.0)
        return a * np.log2(n_safe) + b

    @staticmethod
    def _linear_model(n, a, b):
        return a * n + b

    @staticmethod
    def _n_log_n_model(n, a, b):
        n_safe = np.maximum(n, 1.0)
        return a * n_safe * np.log2(n_safe) + b

    @staticmethod
    def _quadratic_model(n, a, b):
        return a * (n**2) + b

    @classmethod
    def estimate(cls, sizes: List[int], times: List[float]) -> Dict[str, Any]:
        """
        Fits empirical data against theoretical models and returns stats.
        """
        if len(sizes) < 4:
            return {
                "estimated_complexity": "Insufficient Data",
                "confidence_score": 0,
                "fit_scores": {}
            }

        n_arr = np.array(sizes, dtype=float)
        t_arr = np.array(times, dtype=float)

        # Normalize time values to [0, 1] for stable fitting comparison
        t_min, t_max = np.min(t_arr), np.max(t_arr)
        if t_max > t_min:
            t_norm = (t_arr - t_min) / (t_max - t_min)
        else:
            t_norm = np.zeros_like(t_arr)

        models = {
            "O(1)": cls._constant_model,
            "O(log n)": cls._log_model,
            "O(n)": cls._linear_model,
            "O(n log n)": cls._n_log_n_model,
            "O(n²)": cls._quadratic_model
        }

        fit_stats = {}
        
        for name, model in models.items():
            try:
                # Use normalized times for fitting comparison
                popt, _ = curve_fit(model, n_arr, t_norm, maxfev=2000)
                predictions = model(n_arr, *popt)
                
                # Compute MSE of normalized values
                mse = np.mean((t_norm - predictions)**2)
                fit_stats[name] = float(mse)
            except Exception as e:
                logger.debug(f"Failed to fit {name}: {e}")
                fit_stats[name] = 1.0 # High error

        # Determine best fit (lowest MSE)
        best_fit = min(fit_stats, key=fit_stats.get)
        best_mse = fit_stats[best_fit]

        # Compute confidence score based on relative error gap
        # If the best fit is much better than the second best, confidence is high
        sorted_errors = sorted(fit_stats.values())
        if len(sorted_errors) > 1 and sorted_errors[1] > 0:
            # Ratio of best error to second best
            ratio = sorted_errors[0] / sorted_errors[1]
            confidence = (1.0 - ratio) * 100
        else:
            confidence = 50.0

        # Bound confidence
        # Also factor in absolute fit quality (MSE)
        absolute_quality = max(0, 1.0 - best_mse)
        final_confidence = min(99.9, confidence * absolute_quality)

        # Prepare theoretical curve points for the best fit
        popt_actual, _ = curve_fit(models[best_fit], n_arr, t_arr, maxfev=2000)
        predicted_times = models[best_fit](n_arr, *popt_actual).tolist()

        return {
            "estimated_complexity": best_fit,
            "confidence_score": round(float(final_confidence), 2),
            "fit_scores": {k: round(v, 6) for k, v in fit_stats.items()},
            "theoretical_curve": predicted_times
        }
