import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Upload file
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },

  // Query data
  queryData: async (datasetId, question) => {
    const response = await apiClient.post('/query', {
      dataset_id: datasetId,
      question: question,
    });
    
    return response.data;
  },

  // Get datasets
  getDatasets: async () => {
    const response = await apiClient.get('/datasets');
    return response.data;
  },

  // Delete dataset
  deleteDataset: async (datasetId) => {
    const response = await apiClient.delete(`/datasets/${datasetId}`);
    return response.data;
  },
};

// Request interceptor for error handling
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const message = error.response?.data?.detail || error.message || 'An error occurred';
    throw new Error(message);
  }
);