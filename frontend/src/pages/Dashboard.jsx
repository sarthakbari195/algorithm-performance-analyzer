import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { getAlgorithms, getDatasets, runBenchmark } from '../services/api';
import BenchmarkForm from '../components/BenchmarkForm';
import ResultsPanel from '../components/ResultsPanel';
import toast from 'react-hot-toast';
import { LayoutDashboard, Beaker, Terminal, Cpu, Activity } from 'lucide-react';

const Dashboard = () => {
    console.log("Dashboard rendering...");
    const [algorithms, setAlgorithms] = useState([]);
    const [datasets, setDatasets] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState(0);
    const [results, setResults] = useState(null);
    const [activeJobId, setActiveJobId] = useState(null);

    const { state } = useLocation();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [algosRes, datasetsRes] = await Promise.all([
                    getAlgorithms(),
                    getDatasets()
                ]);
                setAlgorithms(algosRes.data);
                setDatasets(datasetsRes.data);
            } catch (error) {
                toast.error("Cloud engine unreachable");
            }
        };
        fetchData();
    }, []);

    const handleBenchmarkSubmit = async (config) => {
        setIsLoading(true);
        setResults(null);
        setProgress(0);

        const toastId = toast.loading('Initializing Research Benchmarks...');

        try {
            const response = await runBenchmark(config, (p) => {
                setProgress(p);
                toast.loading(`Benchmarking: ${p}%`, { id: toastId });
            });

            setResults(response.data);
            setActiveJobId(response.id);
            toast.success("Experiment Analysis Complete", { id: toastId });
        } catch (error) {
            toast.error(error.message || "Benchmark failed", { id: toastId });
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
            {/* Header Section */}
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-6">
                <div className="space-y-2">
                    <div className="flex items-center gap-3 text-indigo-400 font-black text-xs uppercase tracking-[0.2em]">
                        <Beaker size={14} className="animate-pulse" />
                        Research Grade Environment
                    </div>
                    <h1 className="text-4xl font-black text-white tracking-tighter">Algorithm Performance <span className="text-indigo-500">Analyzer</span></h1>
                    <p className="text-gray-500 max-w-2xl font-medium leading-relaxed">
                        Verify empirical time complexity against theoretical growth models using
                        High-Resolution timing and memory tracing.
                    </p>
                </div>

                <div className="flex gap-4">
                    <div className="px-4 py-3 bg-gray-900 border border-gray-800 rounded-2xl flex items-center gap-4">
                        <Terminal size={20} className="text-gray-500" />
                        <div className="text-left">
                            <p className="text-[10px] font-black text-gray-500 uppercase">Engine Status</p>
                            <p className="text-xs font-bold text-emerald-400">READY</p>
                        </div>
                    </div>
                    <div className="px-4 py-3 bg-gray-900 border border-gray-800 rounded-2xl flex items-center gap-4">
                        <Cpu size={20} className="text-gray-500" />
                        <div className="text-left">
                            <p className="text-[10px] font-black text-gray-500 uppercase">Precision</p>
                            <p className="text-xs font-bold text-indigo-400">High Resolution</p>
                        </div>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 xl:grid-cols-12 gap-10">
                {/* Control Panel */}
                <div className="xl:col-span-4 lg:col-span-5">
                    <div className="space-y-6">
                        <BenchmarkForm
                            algorithms={algorithms}
                            datasets={datasets}
                            onSubmit={handleBenchmarkSubmit}
                            isLoading={isLoading}
                            prefill={state?.prefill}
                        />

                        {isLoading && (
                            <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 space-y-4 animate-in fade-in zoom-in duration-300">
                                <div className="flex justify-between items-center text-xs font-black uppercase tracking-wider">
                                    <span className="text-gray-400">Step Progress</span>
                                    <span className="text-indigo-400 font-mono">{progress}%</span>
                                </div>
                                <div className="h-2 w-full bg-gray-800 rounded-full overflow-hidden shadow-inner">
                                    <div
                                        className="h-full bg-indigo-500 transition-all duration-300 ease-out shadow-[0_0_12px_rgba(99,102,241,0.4)]"
                                        style={{ width: `${progress}%` }}
                                    ></div>
                                </div>
                                <p className="text-[10px] text-gray-500 text-center font-bold italic">
                                    Benchmarking in isolated process. Please do not close tab.
                                </p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Main Results Display */}
                <div className="xl:col-span-8 lg:col-span-7">
                    {results ? (
                        <ResultsPanel results={results} jobId={activeJobId} />
                    ) : (
                        <div className="h-full min-h-[500px] border-2 border-dashed border-gray-800 rounded-[3rem] flex flex-col items-center justify-center text-center p-12 group hover:border-indigo-500/30 transition-all duration-500">
                            <div className="w-20 h-20 bg-gray-900 rounded-3xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform shadow-2xl">
                                <Activity className="text-gray-700 group-hover:text-indigo-500 transition-colors" size={32} />
                            </div>
                            <h3 className="text-xl font-bold text-gray-400 mb-2">No active experiment</h3>
                            <p className="text-sm text-gray-600 max-w-xs font-medium">
                                Configure your algorithms and run a benchmark scale analysis to see results.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
