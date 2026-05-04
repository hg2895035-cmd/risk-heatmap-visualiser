import { useState, useEffect } from 'react';
import { getStats } from '../services/api';
import LoadingSkeleton from '../components/LoadingSkeleton';
import ScoreBadge from '../components/ScoreBadge';

export default function Dashboard() {
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

  if (loading) return <LoadingSkeleton />;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Dashboard</h1>

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
          <h3 className="text-lg font-semibold mb-4">Risks by Category</h3>
          <div className="space-y-3">
            {stats?.byCategory && Object.entries(stats.byCategory).map(([category, count]) => (
              <div key={category} className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">{category}</span>
                <div className="flex items-center space-x-3">
                  <div className="w-32 bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary h-2 rounded-full"
                      style={{ width: `${(count / stats.total) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm text-gray-600 w-8">{count}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Risks by Status</h3>
          <div className="space-y-3">
            {stats?.byStatus && Object.entries(stats.byStatus).map(([status, count]) => {
              const colors = {
                LOW: 'bg-green-500',
                MEDIUM: 'bg-yellow-500',
                HIGH: 'bg-orange-500',
                CRITICAL: 'bg-red-500',
              };
              return (
                <div key={status} className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <div className={`w-3 h-3 rounded-full ${colors[status]}`} />
                    <span className="text-sm font-medium text-gray-700">{status}</span>
                  </div>
                  <span className="text-sm text-gray-600">{count}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
