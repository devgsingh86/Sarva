import { PrismaClient } from '@prisma/client';
import jwt from 'jsonwebtoken';

const prisma = new PrismaClient();
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';
const JWT_EXPIRATION = '7d';

export class AuthService {
  generateToken(userId: string): string {
    return jwt.sign({ userId }, JWT_SECRET, { expiresIn: JWT_EXPIRATION });
  }

  generateRefreshToken(userId: string): string {
    return jwt.sign({ userId, type: 'refresh' }, JWT_SECRET, { expiresIn: '30d' });
  }

  async createSession(userId: string) {
    const token = this.generateToken(userId);
    const refreshToken = this.generateRefreshToken(userId);
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 7);

    await prisma.session.create({
      data: { userId, token, refreshToken, expiresAt },
    });

    return { token, refreshToken };
  }

  verifyToken(token: string) {
    try {
      return jwt.verify(token, JWT_SECRET) as { userId: string };
    } catch {
      return null;
    }
  }

  async deleteSession(token: string) {
    await prisma.session.delete({ where: { token } });
  }
}
