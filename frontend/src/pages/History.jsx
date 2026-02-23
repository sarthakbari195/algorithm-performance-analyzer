import React, { useEffect, useState } from 'react';
import { getHistory, deleteExperiment, getCsvUrl } from '../services/api';
import {
    Calendar,
    Box,
    Trash2,
    ExternalLink,
    RefreshCcw,
    FileSpreadsheet,
    Clock,
    TrendingUp,
    ShieldCheck
} from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

const HistoryPage = () => {
    const [history, setHistory] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const navigate = useNavigate();

    const fetchHistory = async () => {
        try {
            const { data } = await getHistory();
            setHistory(data);
        } catch (error) {
            toast.error("Failed to load history");
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    const handleDelete = async (id) => {
        const tId = toast.loading("Deleting experiment...");
        try {
            await deleteExperiment(id);
            setHistory(history.filter(h => h.id !== id));
            toast.success("Deleted successfully", { id: tId });
        } catch (error) {
            toast.error("Failed to delete", { id: tId });
        }
    };

    const handleRerun = (config) => {
        // Redirection with state to prefill dashboard
        navigate('/', { state: { prefill: config } });
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[60vh]">
                <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-black text-white tracking-tight">Experiment History</h1>
                    <p className="text-gray-500 mt-1 font-medium italic">Verified research logs and historical benchmarks.</p>
                </div>
            </header>

            <div className="bg-gray-900 border border-gray-800 rounded-3xl overflow-hidden shadow-2xl">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-gray-800/30 border-b border-gray-800">
                                <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Date / ID</th>
                                <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Configuration</th>
                                <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest">Analysis</th>
                                <th className="px-6 py-4 text-xs font-black text-gray-400 uppercase tracking-widest text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-800/50">
                            {history.length === 0 ? (
                                <tr>
                                    <td colSpan="4" className="px-6 py-20 text-center text-gray-500 font-bold uppercase tracking-widest">
                                        No research data found.
                                    </td>
                                </tr>
                            ) : history.map((exp) => (
                                <tr key={exp.id} className="hover:bg-gray-800/20 transition-colors group">
                                    <td className="px-6 py-6">
                                        <div className="flex items-start gap-3">
                                            <div className="p-2 bg-indigo-500/10 rounded-lg text-indigo-400">
                                                <Calendar size={18} />
                                            </div>
                                            <div>
                                                <div className="text-sm font-bold text-white">
                                                    {exp.timestamp && exp.timestamp !== 'Unknown'
                                                        ? format(new Date(exp.timestamp), 'MMM dd, HH:mm')
                                                        : 'Recent Run'}
                                                </div>
                                                <div className="text-[10px] font-mono text-gray-500 mt-1">
                                                    ID: {exp.id.split('-')[0]}...
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-6">
                                        <div className="space-y-1">
                                            <div className="flex items-center gap-2">
                                                <span className="text-xs font-bold text-gray-300">Mode:</span>
                                                <span className={`text-[10px] px-2 py-0.5 rounded-full font-black uppercase ${exp.mode === 'progressive' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-blue-500/10 text-blue-400'
                                                    }`}>
                                                    {exp.mode}
                                                </span>
                                            </div>
                                            <div className="text-xs text-gray-500">
                                                {exp.config.algorithms.length} Algorithms • {exp.config.dataset}
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-6">
                                        <div className="flex items-center gap-4">
                                            <div className="space-y-1">
                                                <div className="flex items-center gap-2">
                                                    <TrendingUp size={14} className="text-indigo-400" />
                                                    <span className="text-xs font-mono font-bold text-indigo-300">
                                                        {exp.estimated_complexity}
                                                    </span>
                                                </div>
                                                <div className="flex items-center gap-2">
                                                    <ShieldCheck size={14} className="text-emerald-400" />
                                                    <span className="text-[10px] font-black text-gray-500 uppercase">
                                                        {exp.confidence_score}% Confidence
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-6 py-6">
                                        <div className="flex items-center justify-end gap-2">
                                            <button
                                                onClick={() => handleRerun(exp.config)}
                                                className="p-2 hover:bg-indigo-500/10 text-gray-400 hover:text-indigo-400 rounded-lg transition-all"
                                                title="Rerun with this config"
                                            >
                                                <RefreshCcw size={18} />
                                            </button>
                                            <a
                                                href={getCsvUrl(exp.id)}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="p-2 hover:bg-emerald-500/10 text-gray-400 hover:text-emerald-400 rounded-lg transition-all"
                                                title="Download CSV"
                                            >
                                                <FileSpreadsheet size={18} />
                                            </a>
                                            <button
                                                onClick={() => handleDelete(exp.id)}
                                                className="p-2 hover:bg-red-500/10 text-gray-400 hover:text-red-400 rounded-lg transition-all"
                                                title="Delete"
                                            >
                                                <Trash2 size={18} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default HistoryPage;
