<template>
  <div class="review-page">
    <section class="review-hero">
      <div class="review-stats">
        <div class="stat"><span class="stat-num">{{ stats.due_today }}</span><span class="stat-lbl">待复习</span></div>
        <div class="stat"><span class="stat-num">{{ stats.total_cards }}</span><span class="stat-lbl">总卡片</span></div>
        <div class="stat"><span class="stat-num">{{ Math.round(stats.overall_accuracy * 100) }}%</span><span class="stat-lbl">正确率</span></div>
        <div class="stat"><span class="stat-num">{{ stats.review_streak }}</span><span class="stat-lbl">连续天数</span></div>
      </div>
    </section>

    <section class="section" v-if="dueCards.length > 0">
      <div class="section-header">
        <h2>开始复习</h2>
        <span class="meta">{{ currentIndex + 1 }} / {{ dueCards.length }}</span>
      </div>

      <div class="flashcard" @click="flipped = !flipped">
        <div class="card-inner" :class="{ flipped }">
          <div class="card-front">
            <span class="card-type">{{ dueCards[currentIndex]?.card_type }}</span>
            <p class="card-question">{{ dueCards[currentIndex]?.question }}</p>
            <span class="card-hint">点击翻转查看答案</span>
          </div>
          <div class="card-back">
            <p class="card-answer">{{ dueCards[currentIndex]?.answer }}</p>
          </div>
        </div>
      </div>

      <div class="rating-row" v-if="flipped">
        <button v-for="r in ratings" :key="r.value" class="rating-btn" :class="r.cls" @click.stop="rate(r.value)">
          {{ r.label }}
        </button>
      </div>
    </section>

    <section class="section" v-else>
      <div class="empty-state">
        <p>今日没有待复习的卡片</p>
        <button class="primary-btn" @click="generateCards">从知识库生成卡片</button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/api';

const stats = ref({ due_today: 0, total_cards: 0, overall_accuracy: 0, review_streak: 0 });
const dueCards = ref<any[]>([]);
const currentIndex = ref(0);
const flipped = ref(false);

const ratings = [
  { value: 1, label: '忘了', cls: 'hard' },
  { value: 3, label: '有点印象', cls: 'medium' },
  { value: 5, label: '轻松记住', cls: 'easy' },
];

async function fetchDue() {
  const [statsRes, cardsRes] = await Promise.allSettled([
    api.get('/spaced-repetition/stats'),
    api.get('/spaced-repetition/due?max_cards=20'),
  ]);
  if (statsRes.status === 'fulfilled') stats.value = statsRes.value.data;
  if (cardsRes.status === 'fulfilled') dueCards.value = cardsRes.value.data;
}

async function rate(quality: number) {
  const card = dueCards.value[currentIndex.value];
  if (!card) return;
  await api.post('/spaced-repetition/session/answer', { card_id: card.id, quality });
  flipped.value = false;
  if (currentIndex.value < dueCards.value.length - 1) {
    currentIndex.value++;
  } else {
    dueCards.value.splice(currentIndex.value, 1);
    currentIndex.value = Math.max(0, currentIndex.value - 1);
  }
  const statsRes = await api.get('/spaced-repetition/stats');
  stats.value = statsRes.data;
}

async function generateCards() {
  await api.post('/spaced-repetition/cards/generate-from-knowledge');
  await fetchDue();
}

onMounted(fetchDue);
</script>

<style scoped lang="less">
@import '@/styles/global.less';
.review-page { max-width: 600px; margin: 0 auto; }

.review-hero {
  background: linear-gradient(135deg, #1d1d1f, #2c2c2e);
  border-radius: @radius-xl;
  padding: 24px;
  margin-bottom: 20px;
}

.review-stats { display: flex; justify-content: space-around; }
.stat { text-align: center; }
.stat-num { display: block; font-size: 28px; font-weight: 700; color: #f5f5f7; }
.stat-lbl { font-size: 11px; color: rgba(245,245,247,0.5); }

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

.flashcard { perspective: 800px; margin-bottom: 16px; }
.card-inner {
  position: relative;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  transform-style: preserve-3d;
  min-height: 200px;
  cursor: pointer;
  &.flipped { transform: rotateY(180deg); }
}

.card-front, .card-back {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  border-radius: @radius-md;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-front {
  background: @bg-body;
  border: 1px solid @border-light;
}

.card-back {
  background: @primary;
  color: white;
  transform: rotateY(180deg);
}

.card-type {
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: @text-tertiary;
  margin-bottom: 12px;
}

.card-question { font-size: 17px; font-weight: 600; text-align: center; line-height: 1.6; color: @text-primary; }
.card-hint { font-size: 11px; color: @text-tertiary; margin-top: 16px; }
.card-answer { font-size: 15px; text-align: center; line-height: 1.8; }

.rating-row { display: flex; gap: 8px; justify-content: center; }
.rating-btn {
  padding: 8px 20px;
  border: none;
  border-radius: @radius-sm;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all @transition-fast;
  &.hard { background: #ff453a20; color: #ff453a; &:hover { background: #ff453a; color: white; } }
  &.medium { background: #ff9f0a20; color: #ff9f0a; &:hover { background: #ff9f0a; color: white; } }
  &.easy { background: #30d15820; color: #30d158; &:hover { background: #30d158; color: white; } }
}

.empty-state { text-align: center; padding: 32px; color: @text-secondary; }
.primary-btn {
  margin-top: 12px;
  padding: 8px 20px;
  border: none;
  border-radius: @radius-sm;
  background: @primary;
  color: white;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  &:hover { background: @primary-light; }
}
</style>
