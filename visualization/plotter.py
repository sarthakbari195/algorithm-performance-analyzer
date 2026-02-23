import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import Optional

class Plotter:
    """Handles generation of performance graphs."""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # Use a style tailored for clean, professional look
        plt.style.use('ggplot')
        
    def plot_time_vs_size(self, df: pd.DataFrame, title_suffix: str = ""):
        """Plots Execution Time vs Input Size."""
        plt.figure(figsize=(10, 6))
        
        for algo in df['Algorithm'].unique():
            subset = df[df['Algorithm'] == algo].sort_values('Input Size')
            plt.plot(subset['Input Size'], subset['Mean Time (s)'], marker='o', label=algo)
            
        plt.title(f"Execution Time vs Input Size {title_suffix}")
        plt.xlabel("Input Size")
        plt.ylabel("Time (seconds)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        path = os.path.join(self.output_dir, "time_complexity.png")
        plt.savefig(path)
        plt.close()
        return path

    def plot_memory_vs_size(self, df: pd.DataFrame, title_suffix: str = ""):
        """Plots Peak Memory vs Input Size."""
        plt.figure(figsize=(10, 6))
        
        for algo in df['Algorithm'].unique():
            subset = df[df['Algorithm'] == algo].sort_values('Input Size')
            # Convert bytes to MB for readability
            plt.plot(subset['Input Size'], subset['Peak Memory (B)'] / 1024 / 1024, marker='x', label=algo)
            
        plt.title(f"Memory Usage vs Input Size {title_suffix}")
        plt.xlabel("Input Size")
        plt.ylabel("Peak Memory (MB)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        path = os.path.join(self.output_dir, "memory_usage.png")
        plt.savefig(path)
        plt.close()
        return path

    def plot_algorithm_comparison(self, df: pd.DataFrame):
        """Bar chart comparison for the largest input size."""
        plt.figure(figsize=(12, 6))
        
        max_size = df['Input Size'].max()
        subset = df[df['Input Size'] == max_size].sort_values('Mean Time (s)')
        
        bars = plt.bar(subset['Algorithm'], subset['Mean Time (s)'])
        plt.title(f"Algorithm Comparison at Input Size {max_size}")
        plt.xlabel("Algorithm")
        plt.ylabel("Time (seconds)")
        plt.xticks(rotation=45)
        
        # Add value labels on top
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}s',
                    ha='center', va='bottom')
                    
        plt.tight_layout()
        
        path = os.path.join(self.output_dir, "comparison_bar.png")
        plt.savefig(path)
        plt.close()
        return path
