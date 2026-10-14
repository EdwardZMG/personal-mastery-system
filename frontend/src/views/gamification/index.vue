<template>
  <div class="gamification-page">
    <section class="level-hero">
      <div class="level-info">
        <div class="level-number">Lv.{{ level.current_level }}</div>
        <div class="level-title">{{ level.level_title }}</div>
        <div class="xp-progress-wrap">
          <div class="xp-bar"><div class="xp-fill" :style="{ width: xpPercent + '%' }"></div></div>
          <div class="xp-labels">
            <span>{{ level.xp_progress }} XP</span>
            <span>{{ level.xp_to_next_level }} XP</span>
          </div>
        </div>
      </div>
      <div class="stats-row">
        <div class="stat-item">
          <div class="stat-value">{{ level.streak_days }}</div>
          <div class="stat-label">连续天数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ level.longest_streak }}</div>
          <div class="stat-label">最长连续</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ level.total_xp }}</div>
          <div class="stat-label">总经验</div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-header">
        <h2>成就墙</h2>
        <span class="meta">{{ unlockedCount }}/{{ achievements.length }} 已解锁</span>
      </div>
      <div class="ach-grid">
        <div v-for="ach in achievements" :key="ach.id" class="ach-card" :class="{ locked: !ach.unlocked }">
          <div class="ach-icon-wrap">{{ ach.icon }}</div>
          <div class="ach-name">{{ ach.name }}</div>
          <div class="ach-desc">{{ ach.description }}</div>
          <div class="ach-xp" v-if="!ach.unlocked">+{{ ach.xp_reward }} XP</div>
          <div class="ach-status" v-else>已解锁</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import api from '@/api';

const level = ref({ current_level: 1, total_xp: 0, level_title: '成长新手', xp_to_next_level: 100, xp_progress: 0, streak_days: 0, longest_streak: 0 });
const achievements = ref<any[]>([]);

const xpPercent = computed(() => {
  if (!level.value.xp_to_next_level) return 0;
  return Math.min(100, Math.round((level.value.xp_progress / level.value.xp_to_next_level) * 100));
});

const unlockedCount = computed(() => achievements.value.filter(a => a.unlocked).length);

onMounted(async () => {
  const [lvlRes, achRes] = await Promise.allSettled([
    api.get('/gamification/level'),
    api.get('/gamification/achievements'),
  ]);
  if (lvlRes.status === 'fulfilled') level.value = lvlRes.value.data;
  if (achRes.status === 'fulfilled') achievements.value = achRes.value.data;
});
</script>

<style scoped lang="less">
@import '@/styles/global.less';
.gamification-page { max-width: 800px; margin: 0 auto; }

.level-hero {
  background: linear-gradient(135deg, #1d1d1f, #2c2c2e);
  border-radius: @radius-xl;
  padding: 32px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: @shadow-lg;
}

.level-number { font-size: 36px; font-weight: 800; color: @primary-light; }
.level-title { font-size: 16px; color: rgba(245,245,247,0.7); margin: 4px 0 16px; }

.xp-progress-wrap { width: 240px; }
.xp-bar { height: 6px; border-radius: 3px; background: rgba(255,255,255,0.1); overflow: hidden; }
.xp-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, @primary, @primary-light); transition: width 0.6s ease; }
.xp-labels { display: flex; justify-content: space-between; margin-top: 6px; font-size: 11px; color: rgba(245,245,247,0.4); }

.stats-row { display: flex; gap: 24px; }
.stat-item { text-align: center; }
.stat-value { font-size: 24px; font-weight: 700; color: #f5f5f7; }
.stat-label { font-size: 11px; color: rgba(245,245,247,0.5); margin-top: 2px; }

.section {
  background: @bg-card;
  border-radius: @radius-lg;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: @shadow-sm;
}
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.section-header h2 { font-size: 16px; font-weight: 700; }
.meta { font-size: 12px; color: @text-secondary; }

.ach-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
.ach-card {
  padding: 16px;
  border-radius: @radius-md;
  background: @bg-body;
  text-align: center;
  transition: all @transition-normal;
  &.locked { opacity: 0.45; }
  &:hover:not(.locked) { transform: translateY(-2px); box-shadow: @shadow-md; }
}
.ach-icon-wrap { font-size: 28px; margin-bottom: 8px; }
.ach-name { font-size: 13px; font-weight: 600; color: @text-primary; }
.ach-desc { font-size: 11px; color: @text-secondary; margin-top: 4px; }
.ach-xp { font-size: 11px; color: @accent-orange; margin-top: 6px; font-weight: 600; }
.ach-status { font-size: 11px; color: @accent-green; margin-top: 6px; font-weight: 600; }
</style>
