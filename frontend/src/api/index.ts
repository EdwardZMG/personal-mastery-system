import axios from 'axios';
import { message } from 'ant-design-vue';
import router from '@/router';

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 30000,
});

// Request interceptor: attach JWT token
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response interceptor: handle errors
request.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const { response } = error;
    if (!response) {
      message.error('网络连接失败，请检查网络');
      return Promise.reject(error);
    }

    switch (response.status) {
      case 401: {
        // Try refresh token
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken && !error.config._retried) {
          error.config._retried = true;
          try {
            const res = await axios.post(
              `${import.meta.env.VITE_API_BASE_URL}/auth/refresh`,
              { refresh_token: refreshToken },
            );
            const { access_token } = res.data;
            localStorage.setItem('token', access_token);
            error.config.headers.Authorization = `Bearer ${access_token}`;
            return request(error.config);
          } catch {
            localStorage.removeItem('token');
            localStorage.removeItem('refresh_token');
            router.push('/login');
            message.error('登录已过期，请重新登录');
          }
        } else {
          localStorage.removeItem('token');
          localStorage.removeItem('refresh_token');
          router.push('/login');
        }
        break;
      }
      case 403:
        message.error('没有权限访问');
        break;
      case 404:
        message.error('请求的资源不存在');
        break;
      case 500:
        message.error('服务器错误，请稍后再试');
        break;
      default:
        message.error(response.data?.detail || '请求失败');
    }
    return Promise.reject(error);
  },
);

export default request;
