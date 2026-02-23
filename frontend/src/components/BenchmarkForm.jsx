import React, { useState } from 'react';
import { Play, Loader2, FastForward, Activity } from 'lucide-react';
import AlgorithmSelector from './AlgorithmSelector';
import DatasetSelector from './DatasetSelector';
import { clsx } from 'clsx';

const BenchmarkForm = ({ algorithms, datasets, onSubmit, isLoading, prefill }) => {
    const [mode, setMode] = useState('progressive'); // default to advanced mode
    const [selectedAlgorithms, setSelectedAlgorithms] = useState([]);
    const [selectedDataset, setSelectedDataset] = useState('random');
    const [minSize, setMinSize] = useState(100);
    const [maxSize, setMaxSize] = useState(2000); // Decreased from 5000
    const [stepStrategy, setStepStrategy] = useState('linear'); // Changed from exponential
    const [trials, setTrials] = useState(1); // Decreased from 3
    const [validateComplexity, setValidateComplexity] = useState(false); // Default to false for speed

    React.useEffect(() => {
        if (prefill) {
            setMode(prefill.mode || 'progressive');
            setSelectedAlgorithms(prefill.algorithms || []);
            setSelectedDataset(prefill.dataset || 'random');
            setMinSize(prefill.min_size || 100);
            setMaxSize(prefill.max_size || 5000);
            setStepStrategy(prefill.step_strategy || 'linear');
            setTrials(prefill.trials || 3);
            setValidateComplexity(prefill.validate_complexity ?? true);
        }
    }, [prefill]);

    const handleSubmit = () => {
        if (selectedAlgorithms.length === 0) return;

        onSubmit({
            mode,
            algorithms: selectedAlgorithms,
            dataset: selectedDataset,
            min_size: parseInt(minSize),
            max_size: parseInt(maxSize),
            step_strategy: stepStrategy,
            trials: parseInt(trials),
            validate_complexity: validateComplexity
        });
    };

    return (
        <div className="bg-gray-800/50 backdrop-blur-md border border-gray-700 rounded-2xl p-6 shadow-2xl sticky top-8">
            <div className="flex items-center justify-between mb-8">
                <h2 className="text-xl font-bold text-white flex items-center gap-3">
                    <Activity className="text-indigo-500" />
                    Analyzer Config
                </h2>

                {/* Mode Toggle */}
                <div className="flex bg-gray-900/50 p-1 rounded-lg border border-gray-700">
                    <button
                        onClick={() => setMode('single')}
                        className={clsx(
                            "px-3 py-1.5 text-xs font-bold rounded-md transition-all",
                            mode === 'single' ? "bg-indigo-600 text-white shadow-lg" : "text-gray-400 hover:text-white"
                        )}
                    >
                        Single
                    </button>
                    <button
                        onClick={() => setMode('progressive')}
                        className={clsx(
                            "px-3 py-1.5 text-xs font-bold rounded-md transition-all",
                            mode === 'progressive' ? "bg-indigo-600 text-white shadow-lg" : "text-gray-400 hover:text-white"
                        )}
                    >
                        Progressive
                    </button>
                </div>
            </div>

            <div className="space-y-6">
                <AlgorithmSelector
                    algorithms={algorithms}
                    selected={selectedAlgorithms}
                    onChange={setSelectedAlgorithms}
                />

                <DatasetSelector
                    datasets={datasets}
                    selected={selectedDataset}
                    onChange={setSelectedDataset}
                />

                {/* Dynamic Scaling Controls */}
                <div className="grid grid-cols-2 gap-4">
                    {mode === 'progressive' && (
                        <div className="space-y-2">
                            <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Min Size</label>
                            <input
                                type="number"
                                value={minSize}
                                onChange={(e) => setMinSize(e.target.value)}
                                className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-indigo-500 outline-none"
                            />
                        </div>
                    )}
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Max Size</label>
                        <input
                            type="number"
                            value={maxSize}
                            onChange={(e) => setMaxSize(e.target.value)}
                            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:ring-2 focus:ring-indigo-500 outline-none"
                        />
                    </div>
                </div>

                {mode === 'progressive' && (
                    <div className="space-y-2">
                        <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Step Strategy</label>
                        <select
                            value={stepStrategy}
                            onChange={(e) => setStepStrategy(e.target.value)}
                            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white outline-none focus:ring-2 focus:ring-indigo-500"
                        >
                            <option value="linear">Linear (+N)</option>
                            <option value="exponential">Exponential (2^N)</option>
                        </select>
                    </div>
                )}

                <div className="space-y-2">
                    <div className="flex justify-between">
                        <label className="text-xs font-bold text-gray-400 uppercase tracking-wider">Trials per size</label>
                        <span className="text-xs font-bold text-indigo-400">{trials}x</span>
                    </div>
                    <input
                        type="range"
                        min="1"
                        max="20"
                        value={trials}
                        onChange={(e) => setTrials(e.target.value)}
                        className="w-full h-1.5 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                    />
                </div>

                <div className="flex items-center justify-between p-3 bg-gray-900/50 rounded-xl border border-gray-700/50">
                    <div className="flex flex-col">
                        <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Advanced Analysis</span>
                        <span className="text-xs font-bold text-white">Complexity Validation</span>
                    </div>
                    <button
                        onClick={() => setValidateComplexity(!validateComplexity)}
                        className={clsx(
                            "w-12 h-6 rounded-full transition-all relative",
                            validateComplexity ? "bg-indigo-600" : "bg-gray-700"
                        )}
                    >
                        <div className={clsx(
                            "absolute top-1 w-4 h-4 bg-white rounded-full transition-all",
                            validateComplexity ? "left-7" : "left-1"
                        )} />
                    </button>
                </div>

                <button
                    onClick={handleSubmit}
                    disabled={isLoading || selectedAlgorithms.length === 0}
                    className={clsx(
                        "w-full py-4 rounded-xl flex items-center justify-center gap-3 font-black text-sm uppercase tracking-widest transition-all",
                        isLoading || selectedAlgorithms.length === 0
                            ? "bg-gray-700 text-gray-500 cursor-not-allowed"
                            : "bg-indigo-600 hover:bg-indigo-500 text-white shadow-xl shadow-indigo-500/20 active:scale-95"
                    )}
                >
                    {isLoading ? (
                        <>
                            <Loader2 className="animate-spin" size={18} />
                            Executing...
                        </>
                    ) : (
                        <>
                            <Play fill="currentColor" size={16} />
                            Run Experiment
                        </>
                    )}
                </button>
            </div>
        </div>
    );
};

export default BenchmarkForm;
