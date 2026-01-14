import { Request, Response, NextFunction } from 'express';
import { AuthService } from '../services/auth.service';

const authService = new AuthService();

export const authenticate = (req: Request, res: Response, next: NextFunction) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }

  const decoded = authService.verifyToken(token);
  if (!decoded) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }

  (req as any).userId = decoded.userId;
  next();
};
