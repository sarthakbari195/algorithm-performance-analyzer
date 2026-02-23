import React from 'react';
import { clsx } from 'clsx';

const DatasetSelector = ({ datasets, selected, onChange }) => {
    return (
        <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-300">Dataset Distribution</label>
            <div className="flex flex-wrap gap-2">
                {datasets.map((ds) => (
                    <button
                        key={ds.id}
                        onClick={() => onChange(ds.id)}
                        className={clsx(
                            "px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 border",
                            selected === ds.id
                                ? "bg-indigo-600 border-indigo-500 text-white shadow-lg shadow-indigo-500/20"
                                : "bg-gray-800 border-gray-700 text-gray-400 hover:bg-gray-700 hover:text-white hover:border-gray-500"
                        )}
                    >
                        {ds.name}
                    </button>
                ))}
            </div>
        </div>
    );
};

export default DatasetSelector;
