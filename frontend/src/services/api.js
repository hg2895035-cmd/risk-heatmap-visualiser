import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const login = (data) => api.post('/auth/login', data);
export const register = (data) => api.post('/auth/register', data);

export const getRisks = (params) => api.get('/risks', { params });
export const getRisk = (id) => api.get(`/risks/${id}`);
export const createRisk = (data) => api.post('/risks', data);
export const updateRisk = (id, data) => api.put(`/risks/${id}`, data);
export const deleteRisk = (id) => api.delete(`/risks/${id}`);
export const searchRisks = (q) => api.get('/risks/search', { params: { q } });
export const getStats = () => api.get('/risks/stats');
export const exportCsv = () => api.get('/risks/export', { responseType: 'blob' });
export const uploadFile = (id, formData) => api.post(`/risks/${id}/upload`, formData, {
  headers: { 'Content-Type': 'multipart/form-data' }
});

export const describeRisk = (data) => axios.post('/ai/describe', data);
export const getRecommendations = (data) => axios.post('/ai/recommend', data);
export const categoriseRisk = (data) => axios.post('/ai/categorise', data);
export const generateReport = (data) => axios.post('/ai/generate-report', data, {
  headers: { 'Content-Type': 'application/json' }
});
export const queryKnowledge = (data) => axios.post('/ai/query', data);
export const analyseDocument = (data) => axios.post('/ai/analyse-document', data);

export default api;
