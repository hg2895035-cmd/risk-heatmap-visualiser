import { useAuth } from '../context/AuthContext';
import { Link } from 'react-router-dom';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-primary text-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center space-x-8">
            <Link to="/dashboard" className="font-bold text-xl">
              Risk Heatmap
            </Link>
            <div className="hidden md:flex space-x-4">
              <Link to="/dashboard" className="px-3 py-2 rounded hover:bg-primary-600 transition-colors">
                Dashboard
              </Link>
              <Link to="/risks" className="px-3 py-2 rounded hover:bg-primary-600 transition-colors">
                Risks
              </Link>
              <Link to="/analytics" className="px-3 py-2 rounded hover:bg-primary-600 transition-colors">
                Analytics
              </Link>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-sm">{user?.name}</span>
              <span className="px-2 py-1 bg-primary-600 rounded text-xs">{user?.role}</span>
            </div>
            <button
              onClick={logout}
              className="px-3 py-2 rounded hover:bg-primary-600 transition-colors min-h-touch"
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
