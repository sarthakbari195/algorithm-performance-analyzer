import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

class DatabaseManager:
    """Manages SQLite storage for algorithm benchmarking experiments."""

    def __init__(self, db_path: str = "experiments.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS experiments (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    config_json TEXT NOT NULL,
                    results_json TEXT NOT NULL,
                    estimated_complexity TEXT,
                    confidence_score REAL
                )
            """)
            conn.commit()

    def save_experiment(self, experiment_id: str, mode: str, config: Dict, results: Any, complexity: str = None, confidence: float = None):
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO experiments (id, timestamp, mode, config_json, results_json, estimated_complexity, confidence_score) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    experiment_id,
                    datetime.now().isoformat(),
                    mode,
                    json.dumps(config),
                    json.dumps(results),
                    complexity,
                    confidence
                )
            )
            conn.commit()

    def get_history(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM experiments ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            
            history = []
            for row in rows:
                item = dict(row)
                item['config'] = json.loads(item.pop('config_json'))
                # Small optimization: don't load full results for history list
                item.pop('results_json') 
                history.append(item)
            return history

    def get_experiment(self, experiment_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM experiments WHERE id = ?", (experiment_id,))
            row = cursor.fetchone()
            if row:
                item = dict(row)
                item['config'] = json.loads(item.pop('config_json'))
                item['results'] = json.loads(item.pop('results_json'))
                return item
            return None

    def delete_experiment(self, experiment_id: str):
        with self._get_connection() as conn:
            conn.execute("DELETE FROM experiments WHERE id = ?", (experiment_id,))
            conn.commit()
