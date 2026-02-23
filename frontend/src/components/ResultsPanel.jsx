import React from 'react';
import { Download, Activity, TrendingUp, Zap, Database } from 'lucide-react';
import TimeChart from './TimeChart';
import MemoryChart from './MemoryChart';
import { getCsvUrl } from '../services/api';

const ResultsPanel = ({ results, jobId }) => {
    if (!results) return null;

    const handleDownloadCsv = () => {
        window.open(getCsvUrl(jobId), '_blank');
    };

    return (
        <div className="space-y-8 animate-in fade-in slide-in-from-bottom-6 duration-700">
            {/* Summary Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.metrics.map((metric, idx) => {
                    const analysis = results.complexity_analysis?.[metric.algorithm_name];

                    return (
                        <div key={idx} className="group bg-gray-900 border border-gray-800 rounded-3xl p-6 hover:border-indigo-500/50 transition-all shadow-2xl overflow-hidden relative">
                            <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
                                <Activity size={80} className="text-indigo-500" />
                            </div>

                            <div className="relative">
                                <div className="flex items-center justify-between mb-4">
                                    <h4 className="font-black text-lg text-white tracking-tight">{metric.algorithm_name}</h4>
                                    <span className="bg-indigo-600/20 text-indigo-400 text-[10px] font-black px-2 py-0.5 rounded-full border border-indigo-500/30 uppercase">
                                        Active
                                    </span>
                                </div>

                                <div className="grid grid-cols-2 gap-4 mb-6">
                                    <div className="bg-gray-800/40 p-3 rounded-2xl border border-gray-700/50">
                                        <p className="text-[10px] font-bold text-gray-500 uppercase mb-1">Mean Time</p>
                                        <p className="text-sm font-mono text-emerald-400 font-bold">{(metric.mean_time * 1000).toFixed(4)}ms</p>
                                    </div>
                                    <div className="bg-gray-800/40 p-3 rounded-2xl border border-gray-700/50">
                                        <p className="text-[10px] font-bold text-gray-500 uppercase mb-1">Peak RAM</p>
                                        <p className="text-sm font-mono text-amber-400 font-bold">{(metric.peak_memory / 1024).toFixed(2)}KB</p>
                                    </div>
                                </div>

                                {analysis && (
                                    <div className="space-y-3 pt-4 border-t border-gray-800">
                                        <div className="flex justify-between items-center">
                                            <span className="text-xs font-bold text-gray-400">Empirical Complexity</span>
                                            <span className="text-xs font-black text-indigo-300 font-mono">{analysis.estimated_complexity}</span>
                                        </div>
                                        <div className="space-y-1">
                                            <div className="flex justify-between text-[10px] font-black text-gray-500 uppercase">
                                                <span>Confidence</span>
                                                <span>{analysis.confidence_score}%</span>
                                            </div>
                                            <div className="h-1.5 w-full bg-gray-800 rounded-full overflow-hidden">
                                                <div
                                                    className="h-full bg-gradient-to-r from-indigo-600 to-purple-500 transition-all duration-1000 ease-out"
                                                    style={{ width: `${analysis.confidence_score}%` }}
                                                />
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Visual Analytics */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <TimeChart
                    data={results.chart_data}
                    complexityAnalysis={results.complexity_analysis}
                />
                <MemoryChart data={results.chart_data} />
            </div>

            {/* Export Actions */}
            <div className="flex items-center justify-between p-6 bg-gray-900 border border-gray-800 rounded-3xl shadow-xl">
                <div>
                    <h3 className="text-white font-bold text-lg mb-1">Export Research Data</h3>
                    <p className="text-xs text-gray-500">Download formatted CSV containing full trial logs and normalization factors.</p>
                </div>
                <button
                    onClick={handleDownloadCsv}
                    className="flex items-center gap-3 px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-2xl font-bold text-sm transition-all border border-gray-700 shadow-lg hover:shadow-indigo-500/10"
                >
                    <Download size={18} className="text-indigo-400" />
                    Download Raw Dataset
                </button>
            </div>
        </div>
    );
};

export default React.memo(ResultsPanel);
