import React from 'react';
import { Check } from 'lucide-react';
import { clsx } from 'clsx';

const AlgorithmSelector = ({ algorithms, selected, onChange }) => {
    const toggleSelection = (id) => {
        if (selected.includes(id)) {
            onChange(selected.filter((item) => item !== id));
        } else {
            onChange([...selected, id]);
        }
    };

    return (
        <div className="space-y-4">
            <label className="block text-sm font-medium text-gray-300">Select Algorithms</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                {algorithms.map((algo) => (
                    <div
                        key={algo.id}
                        onClick={() => toggleSelection(algo.id)}
                        className={clsx(
                            "cursor-pointer p-3 rounded-lg border transition-all duration-200 flex items-center justify-between group",
                            selected.includes(algo.id)
                                ? "bg-indigo-900/40 border-indigo-500 shadow-md shadow-indigo-500/10"
                                : "bg-gray-800 border-gray-700 hover:border-gray-500 hover:bg-gray-750"
                        )}
                    >
                        <div>
                            <span className={clsx(
                                "font-medium block",
                                selected.includes(algo.id) ? "text-indigo-200" : "text-gray-300 group-hover:text-white"
                            )}>{algo.name}</span>
                            <span className="text-xs text-gray-500">{algo.category}</span>
                        </div>

                        {selected.includes(algo.id) && (
                            <div className="bg-indigo-500 rounded-full p-0.5">
                                <Check size={14} className="text-white" />
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default AlgorithmSelector;
