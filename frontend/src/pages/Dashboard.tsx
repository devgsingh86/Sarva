import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { FaSignOutAlt, FaUser } from 'react-icons/fa';

export const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">Sarva</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">
                {user?.firstName} {user?.lastName}
              </span>
              <button
                onClick={handleLogout}
                className="flex items-center px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
              >
                <FaSignOutAlt className="mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg p-6">
            <div className="flex items-center mb-6">
              <div className="bg-blue-100 rounded-full p-4 mr-4">
                <FaUser className="text-blue-600 text-3xl" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">
                  Welcome, {user?.firstName}!
                </h2>
                <p className="text-gray-600">{user?.email}</p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
              <div className="bg-blue-50 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-blue-800 mb-2">
                  Profile Status
                </h3>
                <p className="text-gray-700">
                  {user?.isVerified ? '✅ Verified' : '⚠️ Not Verified'}
                </p>
              </div>

              <div className="bg-green-50 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-green-800 mb-2">
                  Account Status
                </h3>
                <p className="text-gray-700">
                  {user?.isActive ? '✅ Active' : '❌ Inactive'}
                </p>
              </div>

              <div className="bg-purple-50 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-purple-800 mb-2">
                  Member Since
                </h3>
                <p className="text-gray-700">
                  {user?.createdAt ? new Date(user.createdAt).toLocaleDateString() : 'N/A'}
                </p>
              </div>
            </div>

            <div className="mt-8 p-6 bg-gray-50 rounded-lg">
              <h3 className="text-xl font-semibold mb-4">User Details</h3>
              <pre className="bg-gray-800 text-green-400 p-4 rounded overflow-auto text-sm">
                {JSON.stringify(user, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};
