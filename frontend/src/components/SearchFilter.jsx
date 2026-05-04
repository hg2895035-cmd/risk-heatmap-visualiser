import { useState, useEffect } from 'react';

export default function SearchFilter({ onSearch, onFilterChange }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [status, setStatus] = useState('');

  useEffect(() => {
    const debounce = setTimeout(() => {
      onSearch(searchTerm);
    }, 300);

    return () => clearTimeout(debounce);
  }, [searchTerm, onSearch]);

  const handleStatusChange = (e) => {
    const value = e.target.value;
    setStatus(value);
    onFilterChange({ status: value });
  };

  const handleClear = () => {
    setSearchTerm('');
    setStatus('');
    onSearch('');
    onFilterChange({ status: '' });
  };

  return (
    <div className="flex flex-wrap gap-4 mb-6">
      <input
        type="text"
        placeholder="Search risks..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="flex-1 min-w-[200px] px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch"
      />

      <select
        value={status}
        onChange={handleStatusChange}
        className="px-4 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-primary min-h-touch"
      >
        <option value="">All Status</option>
        <option value="LOW">Low</option>
        <option value="MEDIUM">Medium</option>
        <option value="HIGH">High</option>
        <option value="CRITICAL">Critical</option>
      </select>

      <button
        onClick={handleClear}
        className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50 min-h-touch"
      >
        Clear
      </button>
    </div>
  );
}
