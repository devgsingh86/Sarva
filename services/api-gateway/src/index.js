
const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'api-gateway',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    message: 'Sarva API Gateway',
    version: '0.1.0',
    endpoints: {
      health: '/health',
      auth: '/api/auth',
      wallet: '/api/wallet',
      messaging: '/api/messaging'
    }
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 API Gateway running on http://localhost:${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/health`);
});

