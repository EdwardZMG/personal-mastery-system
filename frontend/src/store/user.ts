import { defineStore } from 'pinia';
import { ref } from 'vue';
import { login as loginApi, getUserInfo, logout as logoutApi, type UserInfo } from '@/api/auth';
import router from '@/router';

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '');
  const userInfo = ref<UserInfo | null>(null);

  async function login(open_id: string) {
    const res = await loginApi({ open_id });
    token.value = res.access_token;
    localStorage.setItem('token', res.access_token);
    localStorage.setItem('refresh_token', res.refresh_token);
    await fetchUserInfo();
  }

  async function fetchUserInfo() {
    try {
      const info = await getUserInfo();
      userInfo.value = info;
    } catch {
      // ignore
    }
  }

  async function logout() {
    try {
      await logoutApi();
    } catch {
      // ignore
    }
    token.value = '';
    userInfo.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    router.push('/login');
  }

  function isLoggedIn(): boolean {
    return !!token.value;
  }

  return {
    token,
    userInfo,
    login,
    fetchUserInfo,
    logout,
    isLoggedIn,
  };
});
