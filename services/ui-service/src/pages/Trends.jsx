import { useState, useEffect } from 'react';
import { getMonthlyRevenue, getYearlyGrowth } from '../services/apiClient';
import DataTable from '../components/DataTable';

const Trends = () => {
  const [monthlyRevenue, setMonthlyRevenue] = useState([]);
  const [yearlyGrowth, setYearlyGrowth] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTrends = async () => {
      try {
        setLoading(true);
        const [revenueRes, growthRes] = await Promise.all([
          getMonthlyRevenue(),
          getYearlyGrowth(),
        ]);

        setMonthlyRevenue(revenueRes.data || []);
        setYearlyGrowth(growthRes.data || []);
        setError(null);
      } catch (err) {
        setError('Failed to load trends. Please try again later.');
        console.error('Error fetching trends:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-800">{error}</p>
      </div>
    );
  }

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Sales Trends</h1>

      <DataTable
        title="Monthly Revenue Timeline"
        data={monthlyRevenue}
        columns={[
          { key: 'year', label: 'Year' },
          {
            key: 'month',
            label: 'Month',
            format: (value) => monthNames[value - 1] || value,
          },
          {
            key: 'revenue',
            label: 'Revenue',
            format: (value) => `$${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
          },
        ]}
      />

      <DataTable
        title="Yearly Growth Summary"
        data={yearlyGrowth}
        columns={[
          { key: 'year', label: 'Year' },
          {
            key: 'total_sales',
            label: 'Total Sales',
            format: (value) => `$${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
          },
          {
            key: 'growth_percent',
            label: 'Growth %',
            format: (value) => value !== null ? `${value.toFixed(2)}%` : 'N/A',
          },
        ]}
      />
    </div>
  );
};

export default Trends;

