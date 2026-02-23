import React from 'react';
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

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const MemoryChart = ({ data }) => {
    if (!data || !data.memory_series) return null;

    const chartData = {
        datasets: data.memory_series.map((series, index) => ({
            label: series.label,
            data: series.data,
            borderColor: `hsl(${index * 137.5 + 40}, 70%, 50%)`,
            backgroundColor: `hsla(${index * 137.5 + 40}, 70%, 50%, 0.5)`,
            tension: 0.3,
            borderWidth: 2,
            pointRadius: 4,
        })),
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: '#9ca3af' } },
            title: {
                display: true,
                text: 'Peak Memory Usage',
                color: '#e5e7eb',
                font: { size: 16 }
            }
        },
        scales: {
            x: {
                type: 'linear',
                title: { display: true, text: 'Input Size (N)', color: '#6b7280' },
                grid: { color: '#374151' },
                ticks: { color: '#9ca3af' }
            },
            y: {
                title: { display: true, text: 'Memory (Bytes)', color: '#6b7280' },
                grid: { color: '#374151' },
                ticks: { color: '#9ca3af' }
            },
        },
    };

    return (
        <div className="h-80 w-full p-4 bg-gray-800/50 rounded-xl border border-gray-700 backdrop-blur-sm">
            <Line options={options} data={chartData} />
        </div>
    );
};

export default MemoryChart;
