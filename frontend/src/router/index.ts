import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: '',
        name: 'Login',
        component: () => import('@/views/auth/login.vue'),
        meta: { title: '登录' },
      },
    ],
  },
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘' },
      },
      {
        path: 'expert',
        name: 'Expert',
        component: () => import('@/views/expert/index.vue'),
        meta: { title: '即时专家' },
      },
      {
        path: 'gamification',
        name: 'Gamification',
        component: () => import('@/views/gamification/index.vue'),
        meta: { title: '成长中心' },
      },
      {
        path: 'spaced-repetition',
        name: 'SpacedRepetition',
        component: () => import('@/views/spaced-repetition/index.vue'),
        meta: { title: '间隔复习' },
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('@/views/knowledge/index.vue'),
        meta: { title: '知识管理' },
      },
      {
        path: 'knowledge/capture',
        name: 'KnowledgeCapture',
        component: () => import('@/views/knowledge/capture.vue'),
        meta: { title: '知识捕获' },
      },
      {
        path: 'knowledge/:id',
        name: 'KnowledgeDetail',
        component: () => import('@/views/knowledge/detail.vue'),
        meta: { title: '知识详情' },
      },
      {
        path: 'learning',
        name: 'Learning',
        component: () => import('@/views/learning/index.vue'),
        meta: { title: '学习内容' },
      },
      {
        path: 'learning/:id',
        name: 'LearningDetail',
        component: () => import('@/views/learning/detail.vue'),
        meta: { title: '学习详情' },
      },
      {
        path: 'review',
        name: 'Review',
        component: () => import('@/views/review/index.vue'),
        meta: { title: '复习管理' },
      },
      {
        path: 'review/:id',
        name: 'ReviewSession',
        component: () => import('@/views/review/session.vue'),
        meta: { title: '复习会话' },
      },
      {
        path: 'speech',
        name: 'Speech',
        component: () => import('@/views/speech/index.vue'),
        meta: { title: '演讲稿管理' },
      },
      {
        path: 'speech/generate',
        name: 'SpeechGenerate',
        component: () => import('@/views/speech/generate.vue'),
        meta: { title: '生成演讲稿' },
      },
      {
        path: 'speech/:id',
        name: 'SpeechDetail',
        component: () => import('@/views/speech/detail.vue'),
        meta: { title: '演讲稿详情' },
      },
      {
        path: 'goals',
        name: 'Goals',
        component: () => import('@/views/goals/index.vue'),
        meta: { title: '目标管理' },
      },
      {
        path: 'habits',
        name: 'Habits',
        component: () => import('@/views/habits/index.vue'),
        meta: { title: '习惯追踪' },
      },
      {
        path: 'classics',
        name: 'Classics',
        component: () => import('@/views/classics/index.vue'),
        meta: { title: '国学经典' },
      },
      {
        path: 'classics/:id',
        name: 'ClassicReader',
        component: () => import('@/views/classics/reader.vue'),
        meta: { title: '经典阅读' },
      },
      {
        path: 'checkin',
        name: 'CheckIn',
        component: () => import('@/views/checkin/index.vue'),
        meta: { title: '每日签到' },
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: { title: '个人中心' },
      },
      {
        path: 'admin',
        name: 'Admin',
        component: () => import('@/views/admin/index.vue'),
        meta: { title: '管理后台' },
      },
      {
        path: 'admin/content',
        name: 'AdminContent',
        component: () => import('@/views/admin/content.vue'),
        meta: { title: '内容管理' },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Auth guard
router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token');
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth) || to.path !== '/login';

  if (to.path === '/login') {
    if (token) {
      next('/dashboard');
    } else {
      next();
    }
    return;
  }

  if (requiresAuth && !token) {
    next('/login');
  } else {
    next();
  }
});

// Update page title
router.afterEach((to) => {
  const title = to.meta.title as string;
  if (title) {
    document.title = `${title} - Edward 个人成长成功系统`;
  }
});

export default router;
