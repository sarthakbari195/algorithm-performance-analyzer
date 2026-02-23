# Algorithm Performance Analyzer

A production-grade full-stack application for benchmarking and analyzing algorithm performance with real-time visualization.

## 🚀 Features

### Backend (Python + FastAPI)
- **Multiple Algorithm Support**: 6 sorting algorithms (Bubble, Insertion, Merge, Quick, Heap, TimSort) and 3 searching algorithms (Linear, Binary, Jump)
- **Precision Benchmarking**: High-precision timing with `time.perf_counter` and memory tracking with `tracemalloc`
- **Statistical Analysis**: Mean, median, standard deviation across multiple trials
- **Complexity Validation**: Empirical Big-O verification using curve fitting
- **Multiple Dataset Types**: Random, Sorted, Reverse Sorted, Nearly Sorted, Few Unique
- **REST API**: FastAPI endpoints with background task processing
- **Export Capabilities**: CSV and JSON result exports

### Frontend (React + Vite + Tailwind CSS)
- **Modern Dashboard**: Clean, dark-mode UI with glassmorphism effects
- **Interactive Configuration**: Multi-select algorithms, dataset picker, input size slider (100 to 1M)
- **Real-time Feedback**: Toast notifications and loading states
- **Dynamic Charts**: Chart.js visualizations for time and memory complexity
- **Responsive Design**: Mobile-friendly layout with bottom navigation
- **History Tracking**: View past benchmark runs
- **Safety Features**: Warnings for large input sizes

## 📂 Project Structure

```
algorithm-performance-analyzer/
├── algorithms/              # Algorithm implementations
│   ├── base.py             # Abstract base classes
│   ├── sorting.py          # Sorting algorithms
│   └── searching.py        # Searching algorithms
│
├── core/                   # Core benchmarking engine
│   ├── benchmark_engine.py # Main benchmarking logic
│   ├── dataset_generator.py # Test data generation
│   ├── complexity_validator.py # Big-O validation
│   └── metrics.py          # Statistical calculations
│
├── visualization/          # Reporting and plotting
│   ├── plotter.py         # Matplotlib charts
│   └── report_generator.py # Markdown reports
│
├── backend/               # FastAPI server
│   └── main.py           # REST API endpoints
│
├── frontend/             # React application
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Dashboard & History
│   │   └── services/    # API client
│   └── package.json
│
├── cli/                  # Command-line interface
│   └── main.py
│
├── results/             # Generated reports and data
└── requirements.txt     # Python dependencies
```

## 🛠️ Installation

### Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd frontend
npm install
```

## 🏃 Running the Application

### Option 1: Full-Stack Web Application

**Terminal 1 - Start Backend:**
```bash
python backend/main.py
```
Backend runs at: `http://localhost:8000`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs at: `http://localhost:5173`

**Access the Application:**
Open your browser to `http://localhost:5173`

### Option 2: Command-Line Interface

Run benchmarks directly from the terminal:

```bash
# Compare all sorting algorithms
python cli/main.py --mode all_sorting --size 10000 --trials 5

# Benchmark specific algorithm
python cli/main.py --algorithm quick_sort --size 100000 --trials 10
```

### Option 3: Docker Deployment

Deploy the full stack using Docker Compose:

```bash
docker-compose up -d --build
```

See [DEPLOYMENT.md](./DEPLOYMENT.md) for more detailed deployment options.

## 📊 API Endpoints

### GET `/algorithms`
Returns list of available algorithms with metadata.

### GET `/datasets`
Returns list of available dataset distributions.

### POST `/benchmark`
Start a new benchmark job.

**Request Body:**
```json
{
  "algorithms": ["quick_sort", "merge_sort"],
  "dataset": "random",
  "max_size": 10000,
  "trials": 5,
  "validate_complexity": false
}
```

**Response:**
```json
{
  "id": "job-uuid",
  "status": "pending"
}
```

### GET `/benchmark/{job_id}`
Get benchmark results (polls until completion).

**Response:**
```json
{
  "id": "job-uuid",
  "status": "completed",
  "metrics": [...],
  "chart_data": {...}
}
```

### GET `/history`
Returns list of completed benchmark runs.

## 🎨 UI Features

### Dashboard
- **Algorithm Selector**: Multi-select with visual feedback
- **Dataset Picker**: Button group for distribution selection
- **Input Size Slider**: Range from 100 to 1,000,000 with warning for large values
- **Trials Selector**: Configure number of statistical trials
- **Complexity Validation**: Optional empirical Big-O verification

### Results Panel
- **Metrics Cards**: Display mean time, peak memory, and complexity class
- **Interactive Charts**: 
  - Time vs Input Size (line chart)
  - Memory vs Input Size (line chart)
- **Export Options**: Download CSV or generate full report

### History Page
- **Tabular View**: Past runs with date, algorithms, dataset, and size
- **Actions**: View details or delete entries

## 📈 Methodology

### Timing & Statistics
- Each algorithm runs N trials (default 5) per input size
- Reports: Mean, Median, Standard Deviation
- Garbage collection invoked before each trial
- Warm-up run to stabilize CPU caches

### Complexity Validation
Fits execution time data against standard complexity curves:
- O(log n)
- O(n)
- O(n log n)
- O(n²)

Uses least-squares curve fitting to determine best match.

### Memory Tracking
- Tracks peak memory usage via `tracemalloc`
- Reports in bytes (convertible to KB/MB in UI)

## 🎯 Example Workflow

1. **Select Algorithms**: Choose Quick Sort, Merge Sort, Bubble Sort
2. **Choose Dataset**: Select "Random"
3. **Set Input Size**: 50,000 elements
4. **Configure Trials**: 5 trials for statistical accuracy
5. **Run Benchmark**: Click "Start Analysis"
6. **View Results**: 
   - Quick Sort and Merge Sort show O(n log n) behavior
   - Bubble Sort shows O(n²) behavior
   - Charts visualize the performance difference
7. **Export**: Download CSV for further analysis

## 🔧 Configuration

### Environment Variables (Frontend)
Create `.env` in `frontend/`:
```
VITE_API_URL=http://localhost:8000
```

### Benchmark Settings
Modify in `cli/main.py` or via API:
- `max_size`: Maximum input size
- `steps`: Number of size increments
- `trials`: Trials per size
- `dataset`: Distribution type

## 🚀 Advanced Features

- **Background Processing**: FastAPI handles benchmarks asynchronously
- **Real-time Polling**: Frontend polls for results every 2 seconds
- **Responsive Charts**: Dynamic color generation using golden angle distribution
- **Dark Mode**: Built-in dark theme optimized for readability
- **Mobile Support**: Fully responsive with bottom navigation

## 📝 Sample Output

### CLI Output
```
Benchmarking Quick Sort with sizes [2000, 4000, 6000, 8000, 10000], trials=5
Benchmarking Quick Sort: 100%|██████████| 5/5

Complexity Validation Results:
Algorithm          Empirical Complexity  Fit Confidence
Quick Sort         O(n log n)           0.95
Bubble Sort        O(n^2)               0.98

Results saved to results/benchmark_results.csv
Report generated at results/PERFORMANCE_REPORT.md
```

### Generated Files
- `results/benchmark_results.csv` - Raw data
- `results/benchmark_results.json` - JSON export
- `results/PERFORMANCE_REPORT.md` - Comprehensive report
- `results/time_complexity.png` - Time chart
- `results/memory_usage.png` - Memory chart
- `results/comparison_bar.png` - Algorithm comparison

## 🤝 Contributing

This is a production-ready framework designed for:
- Algorithm education
- Interview preparation
- Performance research
- Benchmarking experiments

## 📄 License

MIT License

## 🎓 Educational Value

Perfect for:
- Understanding algorithm complexity in practice
- Visualizing Big-O notation
- Comparing sorting/searching strategies
- Learning full-stack development patterns
- Interview preparation for software engineering roles

---

**Built with:** Python, FastAPI, React, Vite, Tailwind CSS, Chart.js, NumPy, Pandas, Matplotlib
