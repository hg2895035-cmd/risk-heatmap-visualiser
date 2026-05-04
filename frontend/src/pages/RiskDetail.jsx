import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getRisk, deleteRisk } from '../services/api';
import { useAuth } from '../context/AuthContext';
import LoadingSkeleton from '../components/LoadingSkeleton';
import StatusBadge from '../components/StatusBadge';
import ScoreBadge from '../components/ScoreBadge';
import AiPanel from '../components/AiPanel';

export default function RiskDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [risk, setRisk] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchRisk();
  }, [id]);

  const fetchRisk = async () => {
    setLoading(true);
    try {
      const response = await getRisk(id);
      setRisk(response.data);
    } catch (err) {
      setError('Failed to load risk details');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this risk?')) return;

    try {
      await deleteRisk(id);
      navigate('/risks');
    } catch (err) {
      alert('Failed to delete risk');
    }
  };

  if (loading) return <LoadingSkeleton />;

  if (error || !risk) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error || 'Risk not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white shadow rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">{risk.title}</h1>
          <div className="flex items-center space-x-4">
            <ScoreBadge score={risk.score} />
            <StatusBadge status={risk.status} />
          </div>
        </div>

        <div className="px-6 py-4 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-500">Category</label>
              <p className="mt-1 text-gray-900">{risk.category}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500">Owner</label>
              <p className="mt-1 text-gray-900">{risk.owner || 'Unassigned'}</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500">Due Date</label>
              <p className="mt-1 text-gray-900">
                {risk.dueDate ? new Date(risk.dueDate).toLocaleDateString() : 'No due date'}
              </p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-500">Created</label>
              <p className="mt-1 text-gray-900">
                {new Date(risk.createdAt).toLocaleDateString()}
              </p>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-500">Description</label>
            <p className="mt-1 text-gray-900">{risk.description || 'No description provided'}</p>
          </div>

          {risk.aiDescription && (
            <div>
              <label className="block text-sm font-medium text-gray-500">AI Description</label>
              <p className="mt-1 text-gray-900 bg-blue-50 p-3 rounded">{risk.aiDescription}</p>
            </div>
          )}

          <AiPanel risk={risk} />
        </div>

        <div className="px-6 py-4 border-t bg-gray-50 flex justify-between">
          <button
            onClick={() => navigate('/risks')}
            className="px-4 py-2 border rounded hover:bg-gray-100 min-h-touch"
          >
            Back to List
          </button>

          {user?.role !== 'VIEWER' && (
            <div className="space-x-2">
              <button
                onClick={() => navigate(`/risks/${id}/edit`)}
                className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-600 min-h-touch"
              >
                Edit
              </button>
              {user?.role === 'ADMIN' && (
                <button
                  onClick={handleDelete}
                  className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 min-h-touch"
                >
                  Delete
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
