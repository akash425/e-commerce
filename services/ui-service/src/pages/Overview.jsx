import { useState, useEffect } from 'react';
import { getTopProducts, getMonthlyRevenue, getYearlyGrowth } from '../services/apiClient';
import StatCard from '../components/StatCard';

const Overview = () => {
  const [topProducts, setTopProducts] = useState([]);
  const [monthlyRevenue, setMonthlyRevenue] = useState([]);
  const [yearlyGrowth, setYearlyGrowth] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [productsRes, revenueRes, growthRes] = await Promise.all([
          getTopProducts(),
          getMonthlyRevenue(),
          getYearlyGrowth(),
        ]);

        setTopProducts(productsRes.data || []);
        setMonthlyRevenue(revenueRes.data || []);
        setYearlyGrowth(growthRes.data || []);
        setError(null);
      } catch (err) {
        setError('Failed to load data. Please try again later.');
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Calculate metrics
  const topProductsCount = topProducts.length;
  
  // Get latest year from yearly growth data
  const latestYear = yearlyGrowth.length > 0 
    ? yearlyGrowth[yearlyGrowth.length - 1]?.year 
    : null;
  
  // Calculate total revenue for latest year
  const latestYearRevenue = latestYear
    ? monthlyRevenue
        .filter(item => item.year === latestYear)
        .reduce((sum, item) => sum + (item.revenue || 0), 0)
    : 0;
  
  // Get latest growth percentage
  const latestGrowthPercent = yearlyGrowth.length > 0 
    ? yearlyGrowth[yearlyGrowth.length - 1]?.growth_percent 
    : null;

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

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Dashboard Overview</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatCard
          title="Top Products"
          value={topProductsCount}
          subtitle="By sales"
        />
        <StatCard
          title="Total Revenue"
          value={`$${latestYearRevenue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`}
          subtitle={latestYear ? `Latest year (${latestYear})` : 'Latest year'}
        />
        <StatCard
          title="Latest Growth"
          value={latestGrowthPercent !== null ? `${latestGrowthPercent.toFixed(1)}%` : 'N/A'}
          subtitle="Year over year"
        />
      </div>
    </div>
  );
};

export default Overview;

