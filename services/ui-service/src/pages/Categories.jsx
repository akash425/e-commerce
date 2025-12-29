import { useState, useEffect } from 'react';
import { getCategoryAvgSales } from '../services/apiClient';
import DataTable from '../components/DataTable';

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setLoading(true);
        const response = await getCategoryAvgSales();
        setCategories(response.data || []);
        setError(null);
      } catch (err) {
        setError('Failed to load categories. Please try again later.');
        console.error('Error fetching categories:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
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

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-800">Category Analytics</h1>

      <DataTable
        title="Category & Subcategory Average Sales"
        data={categories}
        columns={[
          { key: 'category', label: 'Category' },
          { key: 'subcategory', label: 'Sub-Category' },
          {
            key: 'avg_sales',
            label: 'Average Sales',
            format: (value) => `$${value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`,
          },
        ]}
      />
    </div>
  );
};

export default Categories;

