import { Link } from 'react-router-dom';
import StatusBadge from './StatusBadge';
import ScoreBadge from './ScoreBadge';

export default function RiskCard({ risk }) {
  return (
    <Link
      to={`/risks/${risk.id}`}
      className="block bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow p-4 border"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className="font-medium text-gray-900">{risk.title}</h3>
          <p className="text-sm text-gray-500 mt-1">{risk.category}</p>
          {risk.owner && (
            <p className="text-sm text-gray-400 mt-1">Owner: {risk.owner}</p>
          )}
        </div>
        <div className="flex flex-col items-end space-y-2">
          <ScoreBadge score={risk.score} />
          <StatusBadge status={risk.status} />
        </div>
      </div>
      {risk.dueDate && (
        <p className="text-xs text-gray-400 mt-3">
          Due: {new Date(risk.dueDate).toLocaleDateString()}
        </p>
      )}
    </Link>
  );
}
