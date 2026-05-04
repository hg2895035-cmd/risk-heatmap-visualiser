export default function ScoreBadge({ score }) {
  const getColor = (score) => {
    if (score >= 9) return 'bg-red-600 text-white';
    if (score >= 7) return 'bg-orange-500 text-white';
    if (score >= 4) return 'bg-yellow-400 text-gray-900';
    return 'bg-green-400 text-gray-900';
  };

  return (
    <span className={`inline-flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm ${getColor(score)}`}>
      {score}
    </span>
  );
}
