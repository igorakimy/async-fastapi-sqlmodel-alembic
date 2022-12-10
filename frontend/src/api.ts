import axios from 'axios';
import { apiUrl } from '@/env';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IRoleSelect,
  IRoleCreate,
  IRoleUpdate
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    return axios.post(`${apiUrl}/login/token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/users`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/users`, data, authHeaders(token));
  },
  async deleteUser(token: string, userId: number) {
    return axios.delete(`${apiUrl}/users/${userId}`, authHeaders(token))
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/login/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/login/reset-password`, {
      new_password: password,
      token,
    });
  },
  async getRoles(token: string) {
    return axios.get<IRoleSelect[]>(`${apiUrl}/roles`, authHeaders(token));
  },
  async createRole(token: string, data: IRoleCreate) {
    return axios.post(`${apiUrl}/roles`, data, authHeaders(token));
  },
  async updateRole(token: string, roleId: number, data: IRoleUpdate) {
    return axios.put(`${apiUrl}/roles/${roleId}`, data, authHeaders(token));
  },
  async deleteRole(token: string, roleId: number) {
    return axios.delete(`${apiUrl}/roles/${roleId}`, authHeaders(token));
  },
};