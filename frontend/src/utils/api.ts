import axios from 'axios';
import { config } from '../config';

// Create an axios instance with custom config
const api = axios.create({
  baseURL: config.api.baseURL,
  timeout: config.api.timeout,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Log request in development
    if (import.meta.env.DEV) {
      console.log('API Request:', {
        url: config.url,
        method: config.method,
        data: config.data,
      });
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Log response in development
    if (import.meta.env.DEV) {
      console.log('API Response:', {
        url: response.config.url,
        status: response.status,
        data: response.data,
      });
    }
    return response;
  },
  (error) => {
    // Handle specific error cases
    if (error.response) {
      switch (error.response.status) {
        case 400:
          console.error('Bad request:', error.response.data);
          break;
        case 401:
          console.error('Unauthorized');
          break;
        case 404:
          console.error('Not found');
          break;
        case 500:
          console.error('Server error');
          break;
        default:
          console.error('API error:', error.response.status);
      }
    } else if (error.request) {
      console.error('No response received:', error.request);
    } else {
      console.error('Request error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const imageApi = {
  // Upload an image for classification
  uploadImage: async (file: File) => {
    const formData = new FormData();
    formData.append('image', file);
    return api.post('/api/classify', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Get classification history
  getHistory: async () => {
    return api.get('/api/history');
  },
};

export default api; 