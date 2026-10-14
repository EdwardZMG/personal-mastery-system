<template>
  <div class="dashboard">
    <!-- Hero: Level + XP -->
    <section class="hero-card">
      <div class="hero-left">
        <div class="greeting">{{ greeting }}，Edward</div>
        <div class="level-row">
          <span class="level-badge">Lv.{{ level.current_level }}</span>
          <span class="level-title">{{ level.level_title }}</span>
        </div>
        <div class="xp-bar-wrap">
          <div class="xp-bar">
            <div class="xp-fill" :style="{ width: xpPercent + '%' }"></div>
          </div>
          <span class="xp-text">{{ level.total_xp }} / {{ level.xp_to_next_level }} XP</span>
        </div>
      </div>
      <div class="hero-right">
        <div class="streak-ring">
          <svg viewBox="0 0 100 100" class="ring-svg">
            <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(0,113,227,0.1)" stroke-width="6" />
            <circle cx="50" cy="50" r="42" fill="none" stroke="url(#grad)" stroke-width="6"
              stroke-linecap="round" :stroke-dasharray="264" :stroke-dashoffset="264 - (264 * streakProgress / 100)"
              transform="rotate(-90 50 50)" />
            <defs>
              <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#0071e3" />
                <stop offset="100%" stop-color="#2997ff" />
              </linearGradient>
            </defs>
          </svg>
          <div class="streak-number">{{ level.streak_days }}</div>
          <div class="streak-label">连续天数</div>
        </div>
      </div>
    </section>

    <!-- Quick Actions -->
    <section class="quick-actions">
      <div class="action-card" @click="router.push('/expert')">
        <span class="action-emoji">💡</span>
        <span class="action-title">即时专家</span>
        <span class="action-desc">输入词汇，秒变专家</span>
      </div>
      <div class="action-card" @click="router.push('/spaced-repetition')">
        <span class="action-emoji">🧠</span>
        <span class="action-title">开始复习</span>
        <span class="action-desc">{{ reviewStats.due_today }} 张卡片待复习</span>
      </div>
      <div class="action-card" @click="router.push('/checkin')">
        <span class="action-emoji">✅</span>
        <span class="action-title">今日签到</span>
        <span class="action-desc">记录今天的状态</span>
      </div>
      <div class="action-card" @click="router.push('/classics')">
        <span class="action-emoji">📖</span>
        <span class="action-title">国学经典</span>
        <span class="action-desc">每日一篇经典</span>
      </div>
    </section>

    <!-- Today's Quests -->
    <section class="section">
      <div class="section-header">
        <h2 class="section-title">今日任务</h2>
        <span class="section-meta">{{ completedQuests }}/{{ quests.length }} 完成</span>
      </div>
      <div class="quest-list">
        <div v-for="quest in quests" :key="quest.id" class="quest-item" :class="{ done: quest.is_completed }"
          @click="!quest.is_completed && completeQuest(quest.id)">
          <div class="quest-check">
            <CheckCircleOutlined v-if="quest.is_completed" class="quest-done-icon" />
            <div v-else class="quest-circle"></div>
          </div>
          <div class="quest-info">
            <span class="quest-text">{{ quest.description }}</span>
            <span class="quest-type">{{ questTypeLabel(quest.quest_type) }}</span>
          </div>
          <span class="quest-xp">+{{ quest.xp_reward }} XP</span>
        </div>
        <div v-if="quests.length === 0" class="empty-state">
          <span>今日任务已刷新</span>
        </div>
      </div>
    </section>

    <!-- Bottom Row: Stats + Achievements -->
    <div class="bottom-row">
      <section class="section stats-section">
        <div class="section-header">
          <h2 class="section-title">能力雷达</h2>
        </div>
        <div ref="radarChartRef" class="chart-container"></div>
      </section>

      <section class="section achievements-section">
        <div class="section-header">
          <h2 class="section-title">最近成就</h2>
          <router-link to="/gamification" class="section-link">查看全部</router-link>
        </div>
        <div class="achievement-grid">
          <div v-for="ach in recentAchievements" :key="ach.id" class="achievement-item">
            <span class="ach-icon">{{ ach.icon }}</span>
            <div class="ach-info">
              <span class="ach-name">{{ ach.name }}</span>
              <span class="ach-desc">{{ ach.description }}</span>
            </div>
          </div>
          <div v-if="recentAchievements.length === 0" class="empty-state">
            <span>完成更多任务解锁成就</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import { CheckCircleOutlined } from '@ant-design/icons-vue';
import * as echarts from 'echarts';
import api from '@/api';

const router = useRouter();

const level = ref({
  current_level: 1, total_xp: 0, level_title: '成长新手',
  xp_to_next_level: 100, xp_progress: 0, streak_days: 0, longest_streak: 0,
});
const quests = ref<any[]>([]);
const recentAchievements = ref<any[]>([]);
const reviewStats = ref({ due_today: 0, total_cards: 0 });
const radarChartRef = ref<HTMLElement>();
let radarChart: echarts.ECharts | null = null;

const greeting = computed(() => {
  const h = new Date().getHours();
  if (h < 6) return '夜深了';
  if (h < 12) return '早上好';
  if (h < 14) return '中午好';
  if (h < 18) return '下午好';
  return '晚上好';
});

const xpPercent = computed(() => {
  const needed = level.value.xp_to_next_level;
  if (!needed) return 0;
  return Math.min(100, Math.round((level.value.xp_progress / needed) * 100));
});

const streakProgress = computed(() => {
  return Math.min(100, (level.value.streak_days / 30) * 100);
});

const completedQuests = computed(() => quests.value.filter(q => q.is_completed).length);

function questTypeLabel(type: string): string {
  const map: Record<string, string> = { main: '主线', side: '支线', challenge: '挑战' };
  return map[type] || type;
}

async function fetchDashboard() {
  try {
    const [levelRes, questRes, achRes, reviewRes] = await Promise.allSettled([
      api.get('/gamification/level'),
      api.get('/gamification/quests/today'),
      api.get('/gamification/achievements'),
      api.get('/spaced-repetition/stats'),
    ]);
    if (levelRes.status === 'fulfilled') level.value = levelRes.value.data;
    if (questRes.status === 'fulfilled') quests.value = questRes.value.data;
    if (achRes.status === 'fulfilled') {
      recentAchievements.value = achRes.value.data.filter((a: any) => a.unlocked).slice(0, 4);
    }
    if (reviewRes.status === 'fulfilled') reviewStats.value = reviewRes.value.data;
  } catch (e) {
    console.error('Dashboard fetch error:', e);
  }
}

async function completeQuest(questId: string) {
  try {
    await api.post(`/gamification/quests/${questId}/complete`);
    await fetchDashboard();
  } catch (e) {
    console.error('Quest complete error:', e);
  }
}

function initRadarChart() {
  if (!radarChartRef.value) return;
  radarChart = echarts.init(radarChartRef.value);
  radarChart.setOption({
    radar: {
      indicator: [
        { name: '脑力', max: 10 },
        { name: '心力', max: 10 },
        { name: '表达', max: 10 },
        { name: '体能', max: 10 },
        { name: '坚韧', max: 10 },
        { name: '社交', max: 10 },
      ],
      shape: 'circle',
      splitNumber: 4,
      axisName: { color: '#86868b', fontSize: 11, fontWeight: 500 },
      splitLine: { lineStyle: { color: 'rgba(0,0,0,0.06)' } },
      splitArea: { show: false },
      axisLine: { lineStyle: { color: 'rgba(0,0,0,0.08)' } },
    },
    series: [{
      type: 'radar',
      data: [{
        value: [7, 6, 5, 4, 6, 5],
        name: '能力值',
        areaStyle: { color: 'rgba(0, 113, 227, 0.12)' },
        lineStyle: { color: '#0071e3', width: 2 },
        itemStyle: { color: '#0071e3' },
        symbol: 'circle',
        symbolSize: 5,
      }],
    }],
  });
}

onMounted(() => {
  fetchDashboard();
  initRadarChart();
  window.addEventListener('resize', () => radarChart?.resize());
});

onBeforeUnmount(() => {
  radarChart?.dispose();
  window.removeEventListener('resize', () => radarChart?.resize());
});
</script>

<style scoped lang="less">
@import '@/styles/global.less';

.dashboard {
  max-width: 960px;
  margin: 0 auto;
}

// Hero
.hero-card {
  background: linear-gradient(135deg, #1d1d1f 0%, #2c2c2e 100%);
  border-radius: @radius-xl;
  padding: 28px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  box-shadow: @shadow-lg;
}

.hero-left {
  flex: 1;
}

.greeting {
  font-size: 22px;
  font-weight: 700;
  color: #f5f5f7;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.level-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}

.level-badge {
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 6px;
  background: @primary;
  color: white;
  letter-spacing: 0.5px;
}

.level-title {
  font-size: 14px;
  color: rgba(245, 245, 247, 0.7);
  font-weight: 500;
}

.xp-bar-wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.xp-bar {
  flex: 1;
  max-width: 280px;
  height: 6px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.1);
  overflow: hidden;
}

.xp-fill {
  height: 100%;
  border-radius: 3px;
  background: linear-gradient(90deg, @primary, @primary-light);
  transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.xp-text {
  font-size: 12px;
  color: rgba(245, 245, 247, 0.5);
  font-weight: 500;
  white-space: nowrap;
}

.hero-right {
  flex-shrink: 0;
}

.streak-ring {
  width: 96px;
  height: 96px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.ring-svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.streak-number {
  font-size: 26px;
  font-weight: 700;
  color: #f5f5f7;
  line-height: 1;
}

.streak-label {
  font-size: 10px;
  color: rgba(245, 245, 247, 0.5);
  margin-top: 2px;
  font-weight: 500;
}

// Quick Actions
.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.action-card {
  background: @bg-card;
  border-radius: @radius-md;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  cursor: pointer;
  transition: all @transition-normal;
  box-shadow: @shadow-sm;

  &:hover {
    transform: translateY(-2px);
    box-shadow: @shadow-md;
  }
}

.action-emoji {
  font-size: 22px;
  margin-bottom: 4px;
}

.action-title {
  font-size: 13.5px;
  font-weight: 600;
  color: @text-primary;
}

.action-desc {
  font-size: 11.5px;
  color: @text-secondary;
}

// Sections
.section {
  background: @bg-card;
  border-radius: @radius-lg;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: @shadow-sm;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 700;
  color: @text-primary;
  letter-spacing: -0.3px;
}

.section-meta {
  font-size: 12px;
  color: @text-secondary;
  font-weight: 500;
}

.section-link {
  font-size: 12px;
  color: @primary;
  font-weight: 500;
  text-decoration: none;
  &:hover { text-decoration: underline; }
}

// Quests
.quest-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.quest-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 8px;
  border-radius: @radius-sm;
  cursor: pointer;
  transition: background @transition-fast;

  &:hover { background: @bg-body; }
  &.done { opacity: 0.5; cursor: default; }
}

.quest-check {
  flex-shrink: 0;
}

.quest-circle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid @border;
  transition: border-color @transition-fast;
}

.quest-item:hover .quest-circle {
  border-color: @primary;
}

.quest-done-icon {
  font-size: 20px;
  color: @accent-green;
}

.quest-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
}

.quest-text {
  font-size: 13.5px;
  font-weight: 500;
  color: @text-primary;
}

.quest-type {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 4px;
  background: @primary-glow;
  color: @primary;
}

.quest-xp {
  font-size: 12px;
  font-weight: 600;
  color: @accent-orange;
}

// Bottom row
.bottom-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.chart-container {
  height: 220px;
}

.achievement-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.achievement-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: @radius-sm;
  transition: background @transition-fast;
  &:hover { background: @bg-body; }
}

.ach-icon {
  font-size: 24px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: @bg-body;
  border-radius: @radius-sm;
}

.ach-info {
  display: flex;
  flex-direction: column;
}

.ach-name {
  font-size: 13px;
  font-weight: 600;
  color: @text-primary;
}

.ach-desc {
  font-size: 11.5px;
  color: @text-secondary;
}

.empty-state {
  padding: 24px;
  text-align: center;
  color: @text-tertiary;
  font-size: 13px;
}

// Responsive
@media (max-width: 768px) {
  .quick-actions { grid-template-columns: repeat(2, 1fr); }
  .bottom-row { grid-template-columns: 1fr; }
  .hero-card { flex-direction: column; gap: 16px; text-align: center; }
  .xp-bar { max-width: 100%; }
}
</style>
