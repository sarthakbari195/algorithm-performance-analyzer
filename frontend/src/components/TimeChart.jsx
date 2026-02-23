import React, { useState } from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { Info } from 'lucide-react';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const TimeChart = ({ data, complexityAnalysis }) => {
    const [showTheoretical, setShowTheoretical] = useState(true);

    if (!data || !data.time_series) return null;

    const datasets = [];

    data.time_series.forEach((series, idx) => {
        // Empirical Curve
        datasets.push({
            label: `${series.label} (Empirical)`,
            data: series.data,
            borderColor: `hsl(${idx * 137.5}, 70%, 50%)`,
            backgroundColor: `hsl(${idx * 137.5}, 70%, 50%, 0.2)`,
            pointRadius: 4,
            borderWidth: 3,
            tension: 0.3,
        });

        // Theoretical Curve Overlay
        if (showTheoretical && series.theoretical) {
            datasets.push({
                label: `${series.label} (Theoretical Fit)`,
                data: series.data.map((p, i) => ({ x: p.x, y: series.theoretical[i] })),
                borderColor: `hsl(${idx * 137.5}, 70%, 50%, 0.5)`,
                borderDash: [5, 5],
                pointRadius: 0,
                borderWidth: 2,
                tension: 0.3,
                fill: false,
            });
        }
    });

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#9ca3af',
                    font: { weight: 'bold', size: 11 },
                    usePointStyle: true,
                },
            },
            tooltip: {
                backgroundColor: '#111827',
                titleColor: '#6366f1',
                bodyColor: '#fff',
                borderColor: '#374151',
                borderWidth: 1,
                padding: 12,
                callbacks: {
                    label: (context) => {
                        const label = context.dataset.label || '';
                        const value = context.parsed.y;
                        return ` ${label}: ${value.toFixed(6)}s`;
                    }
                }
            },
        },
        scales: {
            x: {
                type: 'linear',
                grid: { color: '#374151', drawBorder: false },
                ticks: { color: '#9ca3af', font: { size: 10 } },
                title: { display: true, text: 'Input Size (N)', color: '#6b7280' }
            },
            y: {
                grid: { color: '#374151', drawBorder: false },
                ticks: {
                    color: '#9ca3af',
                    font: { size: 10 },
                    callback: (val) => val.toFixed(4)
                },
                title: { display: true, text: 'Execution Time (s)', color: '#6b7280' }
            },
        },
    };

    return (
        <div className="bg-gray-800/50 border border-gray-700 rounded-2xl p-6 shadow-xl relative h-[450px]">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-white flex items-center gap-2">
                    Time vs. Scale
                    <span className="text-[10px] bg-gray-900 border border-gray-700 px-2 py-0.5 rounded uppercase tracking-tighter text-gray-400">RESEARCH MODE</span>
                </h3>

                <button
                    onClick={() => setShowTheoretical(!showTheoretical)}
                    className={`text-xs font-bold px-3 py-1.5 rounded-lg border transition-all ${showTheoretical
                            ? 'bg-indigo-600/20 border-indigo-500 text-indigo-400'
                            : 'bg-gray-900 border-gray-700 text-gray-500'
                        }`}
                >
                    Theoretical Overlay
                </button>
            </div>

            <div className="h-[340px]">
                <Line options={options} data={{ datasets }} />
            </div>

            {complexityAnalysis && (
                <div className="mt-4 p-3 bg-indigo-900/20 border border-indigo-500/30 rounded-xl flex items-center gap-3">
                    <Info className="text-indigo-400 shrink-0" size={18} />
                    <div className="text-xs">
                        {Object.entries(complexityAnalysis).map(([algo, meta]) => (
                            <div key={algo} className="flex gap-2 items-center">
                                <span className="font-bold text-white">{algo}:</span>
                                <span className="text-indigo-300 font-mono">Empirical {meta.estimated_complexity}</span>
                                <span className="text-gray-500">|</span>
                                <span className="text-emerald-400 font-bold">Confidence {meta.confidence_score}%</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default TimeChart;
