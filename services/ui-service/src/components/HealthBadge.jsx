import { useState, useEffect } from 'react';
import apiClient from '../services/apiClient';

const HealthBadge = () => {
  const [isHealthy, setIsHealthy] = useState(false);
  const [loading, setLoading] = useState(true);

  const checkHealth = async () => {
    try {
      const response = await apiClient.get('/health');
      setIsHealthy(response.data.status === 'healthy');
      setLoading(false);
    } catch (err) {
      setIsHealthy(false);
      setLoading(false);
    }
  };

  useEffect(() => {
    // Initial check
    checkHealth();

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      checkHealth();
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-600">
        Checking...
      </div>
    );
  }

  return (
    <div
      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
        isHealthy
          ? 'bg-green-100 text-green-800'
          : 'bg-red-100 text-red-800'
      }`}
    >
      {isHealthy ? 'API Healthy' : 'API Down'}
    </div>
  );
};

export default HealthBadge;

