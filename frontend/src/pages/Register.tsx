import { useState, FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { FaUser, FaEnvelope, FaLock, FaPhone } from 'react-icons/fa';

export const Register = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters');
      return;
    }

    setLoading(true);

    try {
      await register({
        firstName: formData.firstName,
        lastName: formData.lastName,
        email: formData.email,
        phone: formData.phone || undefined,
        password: formData.password,
      });
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-500 to-pink-600 py-12">
      <div className="bg-white shadow-2xl rounded-lg px-8 py-10 max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Join Sarva</h1>
          <p className="text-gray-600 mt-2">Create your account</p>
        </div>

        <form onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4 text-sm">
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2">
                First Name
              </label>
              <div className="flex items-center border-b border-gray-300 py-2">
                <FaUser className="text-gray-500 mr-2 text-sm" />
                <input
                  className="appearance-none bg-transparent border-none w-full text-gray-700 py-1 px-1 leading-tight focus:outline-none text-sm"
                  type="text"
                  name="firstName"
                  placeholder="John"
                  value={formData.firstName}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-gray-700 text-sm font-bold mb-2">
                Last Name
              </label>
              <div className="flex items-center border-b border-gray-300 py-2">
                <FaUser className="text-gray-500 mr-2 text-sm" />
                <input
                  className="appearance-none bg-transparent border-none w-full text-gray-700 py-1 px-1 leading-tight focus:outline-none text-sm"
                  type="text"
                  name="lastName"
                  placeholder="Doe"
                  value={formData.lastName}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Email
            </label>
            <div className="flex items-center border-b border-gray-300 py-2">
              <FaEnvelope className="text-gray-500 mr-3" />
              <input
                className="appearance-none bg-transparent border-none w-full text-gray-700 py-1 px-2 leading-tight focus:outline-none"
                type="email"
                name="email"
                placeholder="your@email.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Phone (Optional)
            </label>
            <div className="flex items-center border-b border-gray-300 py-2">
              <FaPhone className="text-gray-500 mr-3" />
              <input
                className="appearance-none bg-transparent border-none w-full text-gray-700 py-1 px-2 leading-tight focus:outline-none"
                type="tel"
                name="phone"
                placeholder="+31 6 1234 5678"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Password
            </label>
            <div className="flex items-center border-b border-gray-300 py-2">
              <FaLock className="text-gray-500 mr-3" />
              <input
                className="appearance-none bg-transparent border-none w-full text-gray-700 py-1 px-2 leading-tight focus:outline-none"
                type="password"
                name="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Confirm Password
            </label>
            <div className="flex items-center border-b border-gray-300 py-2">
              <FaLock className="text-gray-500 mr-3" />
              <input
                className="appearance-none bg-transparent border-none w-full text-gray-700 py-1 px-2 leading-tight focus:outline-none"
                type="password"
                name="confirmPassword"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <button
            className="w-full bg-purple-500 hover:bg-purple-700 text-white font-bold py-3 px-4 rounded focus:outline-none focus:shadow-outline transition duration-200 disabled:opacity-50"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>

          <div className="text-center mt-6">
            <p className="text-gray-600">
              Already have an account?{' '}
              <Link to="/login" className="text-purple-500 hover:text-purple-700 font-semibold">
                Sign in
              </Link>
            </p>
          </div>
        </form>
      </div>
    </div>
  );
};
