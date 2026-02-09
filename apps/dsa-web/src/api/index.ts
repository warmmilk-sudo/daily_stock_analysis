import axios, { AxiosError } from 'axios';
import { API_BASE_URL } from '../utils/constants';
import { useAuthStore } from '../stores/authStore';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor: attach Bearer token
apiClient.interceptors.request.use(
  (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor: handle 401 and other errors
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status;

      if (status === 401) {
        // Token expired or invalid - clear auth and redirect
        console.warn('[API] 401 Unauthorized - logging out');
        useAuthStore.getState().logout();
        // Only redirect if not already on login page
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      } else if (status >= 500) {
        console.error('[API] Server error:', status, error.response.data);
      }
    } else if (error.request) {
      console.error('[API] No response received:', error.message);
    } else {
      console.error('[API] Request setup error:', error.message);
    }

    return Promise.reject(error);
  }
);

export default apiClient;
