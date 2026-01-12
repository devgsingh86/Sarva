const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8001;

app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'auth-service',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Sarva Authentication Service',
    version: '0.1.0',
    endpoints: {
      health: '/health',
      register: 'POST /api/auth/register',
      login: 'POST /api/auth/login',
      verify: 'GET /api/auth/verify'
    }
  });
});

// Auth routes placeholder
app.post('/api/auth/register', (req, res) => {
  res.json({ message: 'Registration endpoint - coming soon' });
});

app.post('/api/auth/login', (req, res) => {
  res.json({ message: 'Login endpoint - coming soon' });
});

app.get('/api/auth/verify', (req, res) => {
  res.json({ message: 'Token verification - coming soon' });
});

app.listen(PORT, () => {
  console.log(`🔐 Auth Service running on http://localhost:${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
});
