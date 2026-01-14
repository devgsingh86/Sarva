import { Request, Response } from 'express';
import { UserService } from '../services/user.service';
import { AuthService } from '../services/auth.service';

const userService = new UserService();
const authService = new AuthService();

export class AuthController {
  async register(req: Request, res: Response) {
    try {
      const { email, phone, password, firstName, lastName } = req.body;

      const existingUser = await userService.findByEmail(email);
      if (existingUser) {
        return res.status(400).json({ error: 'User already exists' });
      }

      const user = await userService.createUser({ email, phone, password, firstName, lastName });
      const { token, refreshToken } = await authService.createSession(user.id);

      res.status(201).json({ message: 'User registered successfully', user, token, refreshToken });
    } catch (error) {
      console.error('Register error:', error);
      res.status(500).json({ error: 'Registration failed' });
    }
  }

  async login(req: Request, res: Response) {
    try {
      const { email, password } = req.body;

      const user = await userService.findByEmail(email);
      if (!user || !(await userService.verifyPassword(user, password))) {
        return res.status(401).json({ error: 'Invalid credentials' });
      }

      const { token, refreshToken } = await authService.createSession(user.id);

      res.json({
        message: 'Login successful',
        user: { id: user.id, email: user.email, firstName: user.firstName, lastName: user.lastName },
        token,
        refreshToken,
      });
    } catch (error) {
      console.error('Login error:', error);
      res.status(500).json({ error: 'Login failed' });
    }
  }

  async logout(req: Request, res: Response) {
    try {
      const token = req.headers.authorization?.replace('Bearer ', '');
      if (token) await authService.deleteSession(token);
      res.json({ message: 'Logout successful' });
    } catch (error) {
      res.status(500).json({ error: 'Logout failed' });
    }
  }

  async me(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const user = await userService.findById(userId);
      res.json({ user });
    } catch (error) {
      res.status(500).json({ error: 'Failed to get user' });
    }
  }
}
