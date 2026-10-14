<template>
  <div class="learning-content">
    <PageHeader title="学习内容" subtitle="个性化推荐与内容库" />
    <a-row :gutter="16">
      <a-col :span="6" v-for="item in contentList" :key="item.id">
        <a-card hoverable @click="goDetail(item.id)" class="content-card">
          <template #title>{{ item.title }}</template>
          <a-tag :color="categoryColor(item.domain)">{{ item.domain }}</a-tag>
          <a-tag>{{ item.content_type }}</a-tag>
          <p class="desc">{{ item.summary }}</p>
          <a-progress :percent="Math.min((item.duration_minutes || 0) / 60 * 100, 100)" :format="() => `${item.duration_minutes || 0}分钟`" size="small" />
        </a-card>
      </a-col>
    </a-row>
    <a-empty v-if="contentList.length === 0" description="暂无内容" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getContentList } from '@/api/learning';
import PageHeader from '@/components/PageHeader.vue';

const router = useRouter();
const contentList = ref<any[]>([]);

const categoryColor = (cat: string) => {
  const map: Record<string, string> = { AI: 'blue', marketing: 'green', chinese_classics: 'red', english: 'orange', speaking: 'purple' };
  return map[cat] || 'default';
};

const goDetail = (id: string) => router.push(`/learning/${id}`);

onMounted(async () => {
  contentList.value = (await getContentList({ limit: 20 })) || [];
});
</script>

<style scoped>
.content-card { margin-bottom: 16px; }
.desc { color: #666; font-size: 13px; margin: 8px 0; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
</style>
