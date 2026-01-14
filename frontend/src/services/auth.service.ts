import { api } from './api.service';

export const authService = {
  async register(data) {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  async login(data) {
    const response = await api.post('/auth/login', data);
    return response.data;
  },

  async logout() {
    await api.post('/auth/logout');
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
  },

  async getMe() {
    const response = await api.get('/auth/me');
    return response.data;
  },

  saveTokens(token, refreshToken) {
    localStorage.setItem('token', token);
    localStorage.setItem('refreshToken', refreshToken);
  },

  getToken() {
    return localStorage.getItem('token');
  },

  isAuthenticated() {
    return !!this.getToken();
  },
};
