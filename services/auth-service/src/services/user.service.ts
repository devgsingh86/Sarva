import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

export class UserService {
  async createUser(data: {
    email: string;
    phone?: string;
    password: string;
    firstName: string;
    lastName: string;
  }) {
    const passwordHash = await bcrypt.hash(data.password, 10);
    
    const user = await prisma.user.create({
      data: {
        email: data.email,
        phone: data.phone,
        passwordHash,
        firstName: data.firstName,
        lastName: data.lastName,
      },
      select: {
        id: true,
        email: true,
        phone: true,
        firstName: true,
        lastName: true,
        isVerified: true,
        createdAt: true,
      },
    });
    
    return user;
  }

  async findByEmail(email: string) {
    return prisma.user.findUnique({ where: { email } });
  }

  async findById(id: string) {
    return prisma.user.findUnique({
      where: { id },
      select: {
        id: true,
        email: true,
        phone: true,
        firstName: true,
        lastName: true,
        isVerified: true,
        isActive: true,
        createdAt: true,
      },
    });
  }

  async verifyPassword(user: any, password: string) {
    return bcrypt.compare(password, user.passwordHash);
  }
}
