import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getRisks, getStats } from '../services/api';
import { useAuth } from '../context/AuthContext';
import LoadingSkeleton from '../components/LoadingSkeleton';
import EmptyState from '../components/EmptyState';
import Pagination from '../components/Pagination';
import SearchFilter from '../components/SearchFilter';
import StatusBadge from '../components/StatusBadge';
import ScoreBadge from '../components/ScoreBadge';

export default function RiskList() {
  const { user } = useAuth();
  const [risks, setRisks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  useEffect(() => {
    fetchRisks();
  }, [page, searchQuery, statusFilter]);

  const fetchRisks = async () => {
    setLoading(true);
    try {
      const params = { page, size: 10, sortBy: 'createdAt', sortDir: 'desc' };
      if (searchQuery) params.q = searchQuery;

      const response = await getRisks(params);
      setRisks(response.data.content);
      setTotalPages(response.data.totalPages);
    } catch (error) {
      console.error('Failed to fetch risks:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await getStats();
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    setPage(0);
  };

  const handleFilterChange = (filters) => {
    setStatusFilter(filters.status || '');
    setPage(0);
  };

  const filteredRisks = statusFilter
    ? risks.filter(r => r.status === statusFilter)
    : risks;

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Risk Items</h1>
        {user?.role !== 'VIEWER' && (
          <Link
            to="/risks/new"
            className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-600 min-h-touch"
          >
            New Risk
          </Link>
        )}
      </div>

      <SearchFilter onSearch={handleSearch} onFilterChange={handleFilterChange} />

      {loading ? (
        <LoadingSkeleton rows={5} />
      ) : filteredRisks.length === 0 ? (
        <EmptyState message="No risks found" />
      ) : (
        <>
          <div className="bg-white shadow-sm rounded-lg overflow-hidden">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Score</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Owner</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Due Date</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredRisks.map((risk) => (
                  <tr key={risk.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{risk.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link to={`/risks/${risk.id}`} className="text-primary hover:underline">
                        {risk.title}
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{risk.category}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <ScoreBadge score={risk.score} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <StatusBadge status={risk.status} />
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{risk.owner || '-'}</td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {risk.dueDate ? new Date(risk.dueDate).toLocaleDateString() : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <Pagination
            currentPage={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
}
