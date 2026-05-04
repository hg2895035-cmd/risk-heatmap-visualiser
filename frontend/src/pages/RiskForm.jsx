import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { createRisk, updateRisk, getRisk } from '../services/api';

const CATEGORIES = ['FINANCIAL', 'OPERATIONAL', 'STRATEGIC', 'COMPLIANCE', 'REPUTATIONAL', 'TECHNOLOGY'];
const STATUSES = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];

export default function RiskForm({ isEdit = false }) {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    category: 'TECHNOLOGY',
    score: 5,
    status: 'LOW',
    owner: '',
    dueDate: '',
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [riskId, setRiskId] = useState(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id');
    if (id) {
      setRiskId(id);
      fetchRisk(id);
    }
  }, []);

  const fetchRisk = async (id) => {
    try {
      const response = await getRisk(id);
      const risk = response.data;
      setFormData({
        title: risk.title || '',
        description: risk.description || '',
        category: risk.category || 'TECHNOLOGY',
        score: risk.score || 5,
        status: risk.status || 'LOW',
        owner: risk.owner || '',
        dueDate: risk.dueDate || '',
      });
    } catch (error) {
      alert('Failed to load risk data');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: null }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.title.trim()) newErrors.title = 'Title is required';
    if (!formData.category) newErrors.category = 'Category is required';
    if (formData.score < 1 || formData.score > 10) newErrors.score = 'Score must be between 1 and 10';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setLoading(true);
    try {
      const payload = {
        ...formData,
        score: parseInt(formData.score),
      };

      if (isEdit && riskId) {
        await updateRisk(riskId, payload);
      } else {
        await createRisk(payload);
      }
      navigate('/risks');
    } catch (error) {
      alert(error.response?.data?.message || 'Failed to save risk');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">
        {isEdit ? 'Edit Risk' : 'Create New Risk'}
      </h1>

      <form onSubmit={handleSubmit} className="bg-white shadow rounded-lg p-6 space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Title *
          </label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className={`w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch ${
              errors.title ? 'border-red-500' : ''
            }`}
            placeholder="Risk title"
          />
          {errors.title && <p className="mt-1 text-sm text-red-500">{errors.title}</p>}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
            className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch"
            placeholder="Describe the risk in detail"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Category *
            </label>
            <select
              name="category"
              value={formData.category}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch"
            >
              {CATEGORIES.map((cat) => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Score (1-10) *
            </label>
            <input
              type="number"
              name="score"
              min="1"
              max="10"
              value={formData.score}
              onChange={handleChange}
              className={`w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch ${
                errors.score ? 'border-red-500' : ''
              }`}
            />
            {errors.score && <p className="mt-1 text-sm text-red-500">{errors.score}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              name="status"
              value={formData.status}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch"
            >
              {STATUSES.map((status) => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Owner
            </label>
            <input
              type="text"
              name="owner"
              value={formData.owner}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch"
              placeholder="Risk owner name"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Due Date
            </label>
            <input
              type="date"
              name="dueDate"
              value={formData.dueDate}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch"
            />
          </div>
        </div>

        <div className="flex justify-end space-x-4 pt-4">
          <button
            type="button"
            onClick={() => navigate('/risks')}
            className="px-6 py-2 border rounded hover:bg-gray-50 min-h-touch"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-primary text-white rounded hover:bg-primary-600 disabled:opacity-50 min-h-touch"
          >
            {loading ? 'Saving...' : isEdit ? 'Update Risk' : 'Create Risk'}
          </button>
        </div>
      </form>
    </div>
  );
}
