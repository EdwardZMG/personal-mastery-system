import request from './index';

export interface LoginParams {
  open_id: string;
}

export interface LoginResult {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface UserInfo {
  user_id: string;
  open_id: string;
  name?: string;
  avatar_url?: string;
  email?: string;
  phone?: string;
  is_active: boolean;
  created_at?: string;
}

export function login(data: LoginParams): Promise<LoginResult> {
  return request.post('/auth/login', data) as any;
}

export function register(data: { open_id: string; name?: string; phone?: string }): Promise<LoginResult> {
  return request.post('/auth/register', data) as any;
}

export function getUserInfo(): Promise<UserInfo> {
  return request.get('/auth/me') as any;
}

export function logout(): Promise<void> {
  return request.post('/auth/logout') as any;
}

export function updateProfile(data: Partial<UserInfo>): Promise<UserInfo> {
  return request.put('/auth/me', data) as any;
}
