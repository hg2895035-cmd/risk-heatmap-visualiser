import { useState, useEffect } from 'react';
import { getStats, exportCsv } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';

export default function Analytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await exportCsv();
      const blob = new Blob([JSON.stringify(response.data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `risks-export-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Export failed:', error);
    }
  };

  if (loading) return <LoadingSkeleton />;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
        <button
          onClick={handleExport}
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-600 min-h-touch"
        >
          Export Data
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500">Total Risks</h3>
          <p className="mt-2 text-3xl font-bold text-gray-900">{stats?.total || 0}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500">High Score (7+)</h3>
          <p className="mt-2 text-3xl font-bold text-orange-600">{stats?.highScoreCount || 0}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500">Overdue</h3>
          <p className="mt-2 text-3xl font-bold text-red-600">{stats?.overdueCount || 0}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-500">Resolved</h3>
          <p className="mt-2 text-3xl font-bold text-green-600">{stats?.resolvedThisMonth || 0}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Distribution by Category</h3>
          <div className="space-y-4">
            {stats?.byCategory && Object.entries(stats.byCategory).map(([category, count]) => {
              const percentage = stats.total ? Math.round((count / stats.total) * 100) : 0;
              return (
                <div key={category}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium">{category}</span>
                    <span className="text-gray-500">{count} ({percentage}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                      className="bg-primary-500 h-4 rounded-full transition-all"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Distribution by Status</h3>
          <div className="space-y-4">
            {stats?.byStatus && Object.entries(stats.byStatus).map(([status, count]) => {
              const percentage = stats.total ? Math.round((count / stats.total) * 100) : 0;
              const colors = {
                LOW: 'bg-green-500',
                MEDIUM: 'bg-yellow-500',
                HIGH: 'bg-orange-500',
                CRITICAL: 'bg-red-500',
              };
              return (
                <div key={status}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="font-medium flex items-center">
                      <span className={`w-3 h-3 rounded-full ${colors[status]} mr-2`} />
                      {status}
                    </span>
                    <span className="text-gray-500">{count} ({percentage}%)</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                      className={`${colors[status]} h-4 rounded-full transition-all`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
