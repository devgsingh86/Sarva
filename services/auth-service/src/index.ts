import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import authRoutes from './routes/auth.routes';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8001;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'auth-service',
    timestamp: new Date().toISOString(),
  });
});

app.use('/api/auth', authRoutes);

app.listen(PORT, () => {
  console.log(`🔐 Auth Service running on http://localhost:${PORT}`);
  console.log(`🏥 Health: http://localhost:${PORT}/health`);
});
