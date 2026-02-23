import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getAlgorithms = () => api.get('/algorithms');
export const getDatasets = () => api.get('/datasets');

export const runBenchmark = async (config, onProgress) => {
    const { data: job } = await api.post('/benchmark', config);
    const jobId = job.id;

    return new Promise((resolve, reject) => {
        const interval = setInterval(async () => {
            try {
                const { data: status } = await api.get(`/status/${jobId}`);

                if (status.progress !== undefined && onProgress) {
                    onProgress(status.progress);
                }

                if (status.status === 'completed') {
                    clearInterval(interval);
                    resolve({ data: status.result, id: jobId });
                } else if (status.status === 'failed') {
                    clearInterval(interval);
                    reject(new Error(status.error || 'Benchmark failed'));
                }
            } catch (error) {
                console.error("Polling error:", error);
                // Keep polling unless it's a 404
                if (error.response?.status === 404) {
                    clearInterval(interval);
                    reject(error);
                }
            }
        }, 1500);
    });
};

export const getHistory = () => api.get('/history');
export const getExperiment = (id) => api.get(`/experiment/${id}`);
export const deleteExperiment = (id) => api.delete(`/experiment/${id}`);
export const getCsvUrl = (id) => `${API_URL}/results/${id}/csv`;
