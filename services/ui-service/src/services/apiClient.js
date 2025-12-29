import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000/api',
});

export const getTopProducts = async () => {
  const response = await apiClient.get('/analytics/top-products');
  return response.data;
};

export const getMonthlyRevenue = async () => {
  const response = await apiClient.get('/analytics/monthly-revenue');
  return response.data;
};

export const getCategoryAvgSales = async () => {
  const response = await apiClient.get('/analytics/category-avg-sales');
  return response.data;
};

export const getYearlyGrowth = async () => {
  const response = await apiClient.get('/analytics/yearly-growth');
  return response.data;
};

export default apiClient;

