import sys
import os
import logging
import uuid
import asyncio
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.benchmark_engine import BenchmarkEngine
from core.dataset_generator import DistributionType
from core.complexity_validator import ComplexityValidator
from core.database import DatabaseManager
from algorithms.sorting import BubbleSort, InsertionSort, MergeSort, QuickSort, HeapSort, TimSort
from algorithms.searching import LinearSearch, BinarySearch, JumpSearch
from visualization.report_generator import ReportGenerator

# Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config from environment
DB_PATH = os.getenv("DATABASE_URL", "experiments.db")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app = FastAPI(title="Advanced Algorithm Performance Analyzer API")
db = DatabaseManager(db_path=DB_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory progress tracking for active jobs
active_jobs = {}

ALGORITHMS = {
    'bubble_sort': {'class': BubbleSort, 'category': 'Sorting'},
    'insertion_sort': {'class': InsertionSort, 'category': 'Sorting'},
    'merge_sort': {'class': MergeSort, 'category': 'Sorting'},
    'quick_sort': {'class': QuickSort, 'category': 'Sorting'},
    'heap_sort': {'class': HeapSort, 'category': 'Sorting'},
    'timsort': {'class': TimSort, 'category': 'Sorting'},
    'linear_search': {'class': LinearSearch, 'category': 'Searching'},
    'binary_search': {'class': BinarySearch, 'category': 'Searching'},
    'jump_search': {'class': JumpSearch, 'category': 'Searching'},
}

class BenchmarkConfig(BaseModel):
    mode: str = "single" # "single" or "progressive"
    algorithms: List[str]
    dataset: str
    min_size: int = 100
    max_size: int = 1000
    step_strategy: str = "linear" # "linear" or "exponential"
    trials: int = 5
    validate_complexity: bool = True
    track_memory: bool = False # Default to false for speed

def run_benchmark_task(job_id: str, config: BenchmarkConfig):
    try:
        engine = BenchmarkEngine()
        active_jobs[job_id]['status'] = 'running'
        
        # Filter and validate algorithms
        selected_algos = []
        for aid in config.algorithms:
            if aid in ALGORITHMS:
                selected_algos.append(ALGORITHMS[aid]['class'])
        
        if not selected_algos:
            raise ValueError("No valid algorithms selected")

        # Generate sizes based on strategy
        sizes = []
        if config.mode == "single":
            sizes = [config.max_size]
        else:
            if config.step_strategy == "linear":
                step = (config.max_size - config.min_size) // 5
                sizes = [config.min_size + step * i for i in range(6)]
            else: # exponential
                curr = config.min_size
                while curr <= config.max_size:
                    sizes.append(curr)
                    curr *= 2
        
        sizes = sorted(list(set(sizes)))
        distribution = DistributionType(config.dataset)
        
        all_metrics = []
        total_steps = len(selected_algos) * len(sizes)
        completed = 0
        
        complexity_analysis = {}

        for algo_cls in selected_algos:
            algo_instance = algo_cls()
            algo_name = algo_instance.name
            complexity = algo_instance.time_complexity
            
            # Safety Check: Skip O(n^2) for large N in Python
            if complexity == "O(n^2)" and config.max_size > 30000:
                logger.warning(f"Skipping {algo_name} - exceeds safety limit for O(n^2)")
                completed += len(sizes)
                continue

            # Research-grade Warm-up (Done once per algorithm, not per size)
            engine.benchmark_algorithm(algo_cls, sizes=[min(config.min_size, 500)], trials=1, distribution=distribution)
            
            algo_metrics = []
            for size in sizes:
                active_jobs[job_id]['progress'] = int((completed / total_steps) * 100)
                
                # Actual measurement (BenchmarkEngine handles the trials)
                res = engine.benchmark_algorithm(algo_cls, sizes=[size], trials=config.trials, distribution=distribution)
                all_metrics.extend(res)
                algo_metrics.extend(res)
                completed += 1
            
            # Analyze complexity if we have enough points
            if len(sizes) >= 4:
                analysis = ComplexityValidator.estimate(
                    [m.input_size for m in algo_metrics],
                    [m.mean_time for m in algo_metrics]
                )
                complexity_analysis[algo_name] = analysis

        # Persistence
        if not os.path.exists("results"): os.makedirs("results")
        
        results_df = pd.DataFrame([m.to_dict() for m in all_metrics])
        report_gen = ReportGenerator(output_dir="results")
        report_path = report_gen.generate_report(results_df, filename=f"report_{job_id}.md")
        csv_path = os.path.join("results", f"results_{job_id}.csv")
        results_df.to_csv(csv_path, index=False)

        final_result = {
            'metrics': [m.to_dict() for m in all_metrics if m.input_size == max(sizes)],
            'complexity_analysis': complexity_analysis,
            'chart_data': {
                'time_series': [
                    {
                        'label': algo_cls().name,
                        'data': [{'x': m.input_size, 'y': m.mean_time} for m in all_metrics if m.algorithm_name == algo_cls().name],
                        'theoretical': complexity_analysis.get(algo_cls().name, {}).get('theoretical_curve')
                    } for algo_cls in selected_algos
                ],
                'memory_series': [
                    {
                        'label': algo_cls().name,
                        'data': [{'x': m.input_size, 'y': m.peak_memory} for m in all_metrics if m.algorithm_name == algo_cls().name]
                    } for algo_cls in selected_algos
                ]
            }
        }

        # Save to SQLite
        db.save_experiment(
            job_id, 
            config.mode, 
            config.dict(), 
            final_result,
            complexity=next(iter(complexity_analysis.values()))['estimated_complexity'] if complexity_analysis else "N/A",
            confidence=next(iter(complexity_analysis.values()))['confidence_score'] if complexity_analysis else 0.0
        )

        active_jobs[job_id]['status'] = 'completed'
        active_jobs[job_id]['result'] = final_result
        active_jobs[job_id]['progress'] = 100

    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}", exc_info=True)
        active_jobs[job_id]['status'] = 'failed'
        active_jobs[job_id]['error'] = str(e)

@app.get("/algorithms")
def get_algorithms():
    return [{'id': k, 'name': v['class']().name, 'category': v['category']} for k, v in ALGORITHMS.items()]

@app.get("/datasets")
def get_datasets():
    return [{'id': d.value, 'name': d.name.replace('_', ' ').title()} for d in DistributionType]

@app.post("/benchmark")
def start_benchmark(config: BenchmarkConfig, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    active_jobs[job_id] = {'status': 'pending', 'progress': 0}
    background_tasks.add_task(run_benchmark_task, job_id, config)
    return {"id": job_id}

@app.get("/status/{job_id}")
def get_status(job_id: str):
    if job_id in active_jobs:
        return active_jobs[job_id]
    # Check DB if not in memory (recovered from restart or just finished)
    exp = db.get_experiment(job_id)
    if exp:
        return {'status': 'completed', 'progress': 100, 'result': exp['results']}
    raise HTTPException(status_code=404, detail="Job not found")

@app.get("/history")
def get_history():
    return db.get_history()

@app.get("/experiment/{exp_id}")
def get_experiment(exp_id: str):
    exp = db.get_experiment(exp_id)
    if not exp: raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@app.delete("/experiment/{exp_id}")
def delete_experiment(exp_id: str):
    db.delete_experiment(exp_id)
    return {"status": "deleted"}

@app.get("/results/{job_id}/csv")
def get_csv(job_id: str):
    path = os.path.join("results", f"results_{job_id}.csv")
    if not os.path.exists(path): raise HTTPException(status_code=404)
    return FileResponse(path, filename=f"results_{job_id}.csv")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
