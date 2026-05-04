import { useState } from 'react';
import { describeRisk, getRecommendations, categoriseRisk } from '../services/api';

export default function AiPanel({ risk }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleDescribe = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await describeRisk({
        title: risk.title,
        description: risk.description,
        category: risk.category,
        score: risk.score,
      });
      setResult({ type: 'description', data: response.data });
    } catch (err) {
      setError('AI analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleRecommend = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await getRecommendations({
        category: risk.category,
        score: risk.score,
        description: risk.description,
      });
      setResult({ type: 'recommendations', data: response.data });
    } catch (err) {
      setError('Failed to get recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCategorise = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await categoriseRisk({
        title: risk.title,
        description: risk.description,
      });
      setResult({ type: 'categorisation', data: response.data });
    } catch (err) {
      setError('Categorisation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4">AI Analysis</h3>

      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={handleDescribe}
          disabled={loading}
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-600 disabled:opacity-50 min-h-touch"
        >
          Describe
        </button>
        <button
          onClick={handleRecommend}
          disabled={loading}
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-600 disabled:opacity-50 min-h-touch"
        >
          Recommend
        </button>
        <button
          onClick={handleCategorise}
          disabled={loading}
          className="px-4 py-2 bg-primary text-white rounded hover:bg-primary-600 disabled:opacity-50 min-h-touch"
        >
          Categorise
        </button>
      </div>

      {loading && (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-4 border-primary border-t-transparent"></div>
          <span className="ml-3">Analyzing...</span>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
          {error}
          <button
            onClick={() => setError(null)}
            className="ml-2 font-bold"
          >
            Retry
          </button>
        </div>
      )}

      {result && (
        <div className="bg-white border rounded-lg p-4">
          {result.type === 'description' && (
            <div>
              <h4 className="font-medium mb-2">AI Description</h4>
              <p className="text-gray-700">{result.data.description}</p>
            </div>
          )}

          {result.type === 'recommendations' && (
            <div>
              <h4 className="font-medium mb-2">Recommendations</h4>
              <ul className="list-disc list-inside space-y-2">
                {result.data.recommendations?.map((rec, idx) => (
                  <li key={idx} className="text-gray-700">
                    <span className="font-medium">[{rec.priority}]</span> {rec.description}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result.type === 'categorisation' && (
            <div>
              <h4 className="font-medium mb-2">Categorisation</h4>
              <p className="text-gray-700">
                Category: <span className="font-semibold">{result.data.category}</span>
              </p>
              <p className="text-gray-700">
                Confidence: {result.data.confidence}%
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
