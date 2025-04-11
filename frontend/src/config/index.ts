export const config = {
  api: {
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    timeout: Number(import.meta.env.VITE_API_TIMEOUT) || 10000,
  },
} as const; 