<template>
  <div class="classics-reader">
    <PageHeader :title="classicName" subtitle="经典阅读与学习" />
    <a-card>
      <a-select v-model:value="currentChapter" style="width: 200px; margin-bottom: 16px" @change="loadChapter">
        <a-select-option v-for="ch in chapters" :key="ch.number" :value="ch.number">第{{ ch.number }}章 {{ ch.name }}</a-select-option>
      </a-select>
      <a-card v-if="progress" style="margin-top: 16px">
        <h3>原文</h3>
        <p class="original-text">{{ progress.original_text || '暂无原文' }}</p>
        <a-divider />
        <h3>译文</h3>
        <p>{{ progress.translation || '暂无译文' }}</p>
        <a-divider />
        <h3>解读</h3>
        <p>{{ progress.interpretation || '暂无解读' }}</p>
        <a-divider />
        <a-row :gutter="16">
          <a-col :span="12">
            <span>掌握度：</span>
            <a-progress :percent="Math.round((progress.mastery_level || 0) * 100)" :stroke-color="'#cf1322'" />
          </a-col>
          <a-col :span="12">
            <a-tag :color="progress.status === 'completed' ? 'green' : 'blue'">{{ progress.status }}</a-tag>
            <span>复习次数: {{ progress.review_count || 0 }}</span>
          </a-col>
        </a-row>
        <a-button type="primary" style="margin-top: 16px" @click="markRead">标记为已读</a-button>
      </a-card>
      <a-empty v-else description="选择章节开始阅读" />
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getClassicProgress, updateProgress } from '@/api/classics';
import PageHeader from '@/components/PageHeader.vue';
import { message } from 'ant-design-vue';

const route = useRoute();
const classicName = route.params.id as string;
const chapters = ref<any[]>([]);
const currentChapter = ref<number | null>(null);
const progress = ref<any>(null);

onMounted(async () => {
  try {
    const res = await getClassicProgress(classicName);
    const data = res || {};
    chapters.value = data.chapters || Array.from({ length: 10 }, (_, i) => ({ number: i + 1, name: `第${i+1}章` }));
  } catch { chapters.value = Array.from({ length: 10 }, (_, i) => ({ number: i + 1, name: `第${i+1}章` })); }
});

const loadChapter = async (chNum: number) => {
  progress.value = { classic_name: classicName, chapter_number: chNum, status: 'not_started', mastery_level: 0, review_count: 0 };
};

const markRead = async () => {
  if (!progress.value) return;
  await updateProgress({ ...progress.value, status: 'reading', mastery_level: Math.min((progress.value.mastery_level || 0) + 0.1, 1) });
  message.success('进度已更新');
};
</script>

<style scoped>
.original-text { font-size: 18px; line-height: 2; color: #333; font-family: 'KaiTi', 'STKaiti', serif; }
</style>
