<template>
  <a-layout class="default-layout">
    <a-layout-sider
      v-model:collapsed="appStore.sidebarCollapsed"
      :trigger="null"
      collapsible
      :width="220"
      class="layout-sider"
    >
      <div class="logo" @click="router.push('/dashboard')">
        <div class="logo-icon">E</div>
        <transition name="fade">
          <span v-if="!appStore.sidebarCollapsed" class="logo-text">成长系统</span>
        </transition>
      </div>

      <nav class="sidebar-nav">
        <a
          v-for="item in navItems"
          :key="item.key"
          class="nav-item"
          :class="{ active: isActive(item.key) }"
          @click="navigate(item)"
        >
          <component :is="item.icon" class="nav-icon" />
          <transition name="fade">
            <span v-if="!appStore.sidebarCollapsed" class="nav-label">{{ item.label }}</span>
          </transition>
          <transition name="fade">
            <span v-if="!appStore.sidebarCollapsed && item.badge" class="nav-badge">{{ item.badge }}</span>
          </transition>
        </a>
      </nav>

      <div class="sidebar-footer">
        <div class="nav-item" @click="handleLogout">
          <LogoutOutlined class="nav-icon" />
          <transition name="fade">
            <span v-if="!appStore.sidebarCollapsed" class="nav-label">退出</span>
          </transition>
        </div>
      </div>
    </a-layout-sider>

    <a-layout class="main-area">
      <header class="top-bar">
        <div class="top-bar-left">
          <component
            :is="appStore.sidebarCollapsed ? MenuUnfoldOutlined : MenuFoldOutlined"
            class="collapse-btn"
            @click="appStore.toggleSidebar()"
          />
          <span class="page-title">{{ currentPageTitle }}</span>
        </div>
        <div class="top-bar-right">
          <div class="quick-expert" @click="router.push('/expert')">
            <span class="qe-icon">💡</span>
            <span class="qe-text">即时专家</span>
          </div>
          <a-dropdown>
            <div class="user-chip">
              <div class="user-avatar">{{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() || 'E' }}</div>
            </div>
            <template #overlay>
              <a-menu>
                <a-menu-item key="profile" @click="router.push('/profile')">
                  <UserOutlined /> 个人中心
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item key="logout" @click="handleLogout">
                  <LogoutOutlined /> 退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>
        </div>
      </header>

      <a-layout-content class="page-content">
        <router-view v-slot="{ Component }">
          <transition name="slide-up" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAppStore } from '@/store/app';
import { useUserStore } from '@/store/user';
import {
  DashboardOutlined,
  BookOutlined,
  ReadOutlined,
  ReloadOutlined,
  AimOutlined,
  CheckCircleOutlined,
  CalendarOutlined,
  UserOutlined,
  SettingOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  LogoutOutlined,
  ThunderboltOutlined,
} from '@ant-design/icons-vue';
import { h } from 'vue';

const router = useRouter();
const route = useRoute();
const appStore = useAppStore();
const userStore = useUserStore();

interface NavItem {
  key: string;
  label: string;
  icon: any;
  path: string;
  badge?: string;
  section?: string;
}

const navItems: NavItem[] = [
  { key: 'dashboard', label: '仪表盘', icon: DashboardOutlined, path: '/dashboard', section: '核心' },
  { key: 'expert', label: '即时专家', icon: ThunderboltOutlined, path: '/expert', badge: 'NEW' },
  { key: 'gamification', label: '成长中心', icon: ThunderboltOutlined, path: '/gamification' },
  { key: 'learning', label: '学习内容', icon: ReadOutlined, path: '/learning' },
  { key: 'spaced-repetition', label: '间隔复习', icon: ReloadOutlined, path: '/spaced-repetition' },
  { key: 'goals', label: '目标', icon: AimOutlined, path: '/goals' },
  { key: 'habits', label: '习惯', icon: CheckCircleOutlined, path: '/habits' },
  { key: 'classics', label: '国学经典', icon: BookOutlined, path: '/classics' },
  { key: 'checkin', label: '签到', icon: CalendarOutlined, path: '/checkin' },
  { key: 'profile', label: '我的', icon: UserOutlined, path: '/profile' },
];

const currentPageTitle = computed(() => {
  const item = navItems.find(i => route.path.startsWith(i.path));
  return item?.label || route.meta?.title as string || '';
});

function isActive(key: string): boolean {
  const item = navItems.find(i => i.key === key);
  if (!item) return false;
  return route.path === item.path || route.path.startsWith(item.path + '/');
}

function navigate(item: NavItem) {
  router.push(item.path);
}

function handleLogout() {
  userStore.logout();
}

onMounted(() => {
  userStore.fetchUserInfo();
});
</script>

<style scoped lang="less">
@import '@/styles/global.less';

.default-layout {
  min-height: 100vh;
}

.layout-sider {
  background: @bg-sidebar;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  flex-direction: column;
  overflow: hidden;

  :deep(.ant-layout-sider-children) {
    display: flex;
    flex-direction: column;
  }
}

.logo {
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  gap: 10px;
  cursor: pointer;
  flex-shrink: 0;
}

.logo-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, @primary, @primary-light);
  color: white;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.logo-text {
  color: @text-inverse;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: -0.3px;
  white-space: nowrap;
}

.sidebar-nav {
  flex: 1;
  padding: 8px 0;
  overflow-y: auto;
  overflow-x: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 9px 16px;
  margin: 1px 8px;
  border-radius: @radius-sm;
  color: @text-inverse-secondary;
  cursor: pointer;
  transition: all @transition-fast;
  gap: 10px;
  text-decoration: none;
  position: relative;

  &:hover {
    background: @bg-sidebar-hover;
    color: @text-inverse;
  }

  &.active {
    background: @bg-sidebar-active;
    color: @primary-light;
    font-weight: 500;
  }
}

.nav-icon {
  font-size: 17px;
  flex-shrink: 0;
  width: 20px;
  text-align: center;
}

.nav-label {
  font-size: 13.5px;
  white-space: nowrap;
  letter-spacing: -0.1px;
}

.nav-badge {
  margin-left: auto;
  font-size: 10px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 4px;
  background: @accent-green;
  color: white;
  letter-spacing: 0.5px;
}

.sidebar-footer {
  padding: 8px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.main-area {
  background: @bg-body;
}

.top-bar {
  height: 52px;
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid @border-light;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.collapse-btn {
  font-size: 16px;
  color: @text-secondary;
  cursor: pointer;
  transition: color @transition-fast;
  &:hover { color: @primary; }
}

.page-title {
  font-size: 15px;
  font-weight: 600;
  color: @text-primary;
  letter-spacing: -0.3px;
}

.top-bar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.quick-expert {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  border-radius: 20px;
  background: @primary-glow;
  color: @primary;
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all @transition-fast;

  &:hover {
    background: @primary;
    color: white;
  }
}

.qe-icon {
  font-size: 14px;
}

.user-chip {
  cursor: pointer;
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, @primary, @accent-purple);
  color: white;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-content {
  padding: 24px;
  min-height: calc(100vh - 52px);
}
</style>
