import React from 'react';

const ProgressBar = ({ progress = 0 }) => {
    return (
        <div className="w-full bg-gray-700 rounded-full h-2.5 mb-4 overflow-hidden">
            <div
                className="bg-indigo-600 h-2.5 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${Math.min(100, Math.max(0, progress))}%` }}
            ></div>
        </div>
    );
};

export default ProgressBar;
