<template>
  <div class="expert-page">
    <div class="expert-hero">
      <h1 class="hero-title">即时专家</h1>
      <p class="hero-desc">输入任何陌生词汇，秒生成专业解读，让你在任何场合都像该领域的专家</p>
    </div>

    <div class="input-section">
      <div class="input-wrap">
        <input
          v-model="keyword"
          class="expert-input"
          placeholder="输入你想了解的词汇... 如 RAG、Agent、量子计算"
          @keyup.enter="generate"
          :disabled="loading"
        />
        <button class="generate-btn" @click="generate" :disabled="loading || !keyword.trim()">
          <span v-if="!loading">生成解读</span>
          <span v-else class="loading-dots">生成中<span>.</span><span>.</span><span>.</span></span>
        </button>
      </div>
      <div class="input-hint">
        <span>试试：</span>
        <span v-for="tag in quickTags" :key="tag" class="quick-tag" @click="keyword = tag">{{ tag }}</span>
      </div>
    </div>

    <transition name="slide-up">
      <div v-if="result" class="result-card">
        <div class="result-header">
          <span class="result-keyword">{{ result.keyword }}</span>
          <button class="copy-btn" @click="copyResult">
            {{ copied ? '已复制' : '复制' }}
          </button>
        </div>
        <p class="result-text">{{ result.explanation }}</p>
        <div class="result-footer">
          <span class="result-time">{{ formatTime(result.generated_at) }}</span>
          <span class="result-saved">已保存到知识库</span>
        </div>
      </div>
    </transition>

    <div v-if="history.length > 0" class="history-section">
      <h3 class="history-title">历史记录</h3>
      <div class="history-list">
        <div v-for="item in history" :key="item.created_at" class="history-item" @click="keyword = item.keyword; generate()">
          <span class="history-keyword">{{ item.keyword }}</span>
          <span class="history-text">{{ item.explanation?.slice(0, 60) }}...</span>
          <span class="history-time">{{ formatTime(item.created_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/api';

const keyword = ref('');
const result = ref<any>(null);
const loading = ref(false);
const copied = ref(false);
const history = ref<any[]>([]);

const quickTags = ['RAG', 'AI Agent', '量子计算', '区块链', 'Web3', '大模型', '数字孪生', '低代码'];

async function generate() {
  if (!keyword.value.trim() || loading.value) return;
  loading.value = true;
  result.value = null;
  try {
    const res = await api.post('/expert/', { keyword: keyword.value.trim() });
    result.value = res.data;
    fetchHistory();
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
}

async function fetchHistory() {
  try {
    const res = await api.get('/expert/history');
    history.value = res.data;
  } catch (e) { /* ignore */ }
}

async function copyResult() {
  if (!result.value) return;
  try {
    await navigator.clipboard.writeText(result.value.explanation);
    copied.value = true;
    setTimeout(() => copied.value = false, 2000);
  } catch (e) { /* fallback */ }
}

function formatTime(iso: string): string {
  if (!iso) return '';
  const d = new Date(iso);
  const now = new Date();
  const diff = now.getTime() - d.getTime();
  if (diff < 60000) return '刚刚';
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前';
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前';
  return d.toLocaleDateString('zh-CN');
}

onMounted(() => fetchHistory());
</script>

<style scoped lang="less">
@import '@/styles/global.less';

.expert-page {
  max-width: 640px;
  margin: 0 auto;
}

.expert-hero {
  text-align: center;
  margin-bottom: 32px;
}

.hero-title {
  font-size: 28px;
  font-weight: 700;
  color: @text-primary;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.hero-desc {
  font-size: 14px;
  color: @text-secondary;
  line-height: 1.6;
}

.input-section {
  margin-bottom: 24px;
}

.input-wrap {
  display: flex;
  gap: 8px;
  background: @bg-card;
  border-radius: @radius-lg;
  padding: 6px;
  box-shadow: @shadow-md;
  border: 1px solid @border-light;
  transition: border-color @transition-fast, box-shadow @transition-fast;

  &:focus-within {
    border-color: @primary;
    box-shadow: @shadow-glow;
  }
}

.expert-input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  padding: 10px 14px;
  background: transparent;
  color: @text-primary;
  font-family: @font-sans;

  &::placeholder { color: @text-tertiary; }
}

.generate-btn {
  padding: 10px 20px;
  border: none;
  border-radius: @radius-md;
  background: @primary;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all @transition-fast;
  white-space: nowrap;

  &:hover:not(:disabled) { background: @primary-light; }
  &:disabled { opacity: 0.5; cursor: not-allowed; }
}

.loading-dots span {
  animation: blink 1.4s infinite both;
  &:nth-child(2) { animation-delay: 0.2s; }
  &:nth-child(3) { animation-delay: 0.4s; }
}

@keyframes blink {
  0%, 80%, 100% { opacity: 0; }
  40% { opacity: 1; }
}

.input-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 10px;
  font-size: 12px;
  color: @text-tertiary;
  flex-wrap: wrap;
}

.quick-tag {
  padding: 3px 10px;
  border-radius: 12px;
  background: @bg-body;
  color: @text-secondary;
  cursor: pointer;
  transition: all @transition-fast;
  font-size: 11.5px;

  &:hover {
    background: @primary-glow;
    color: @primary;
  }
}

.result-card {
  background: @bg-card;
  border-radius: @radius-lg;
  padding: 24px;
  box-shadow: @shadow-md;
  margin-bottom: 24px;
  border-left: 3px solid @primary;
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.result-keyword {
  font-size: 18px;
  font-weight: 700;
  color: @text-primary;
}

.copy-btn {
  padding: 4px 12px;
  border: 1px solid @border;
  border-radius: 6px;
  background: transparent;
  color: @text-secondary;
  font-size: 12px;
  cursor: pointer;
  transition: all @transition-fast;

  &:hover {
    border-color: @primary;
    color: @primary;
  }
}

.result-text {
  font-size: 15px;
  line-height: 1.8;
  color: @text-primary;
  margin-bottom: 14px;
}

.result-footer {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 11.5px;
  color: @text-tertiary;
}

.result-saved {
  color: @accent-green;
}

.history-section {
  margin-top: 8px;
}

.history-title {
  font-size: 14px;
  font-weight: 600;
  color: @text-secondary;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.history-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: @radius-sm;
  cursor: pointer;
  transition: background @transition-fast;

  &:hover { background: @bg-card; }
}

.history-keyword {
  font-size: 13px;
  font-weight: 600;
  color: @primary;
  min-width: 80px;
}

.history-text {
  flex: 1;
  font-size: 12.5px;
  color: @text-secondary;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.history-time {
  font-size: 11px;
  color: @text-tertiary;
  white-space: nowrap;
}
</style>
