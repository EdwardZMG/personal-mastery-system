<template>
  <div class="learning-detail">
    <PageHeader :title="content.title || '内容详情'" :subtitle="content.domain" />
    <a-card v-if="content.id">
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="标题">{{ content.title }}</a-descriptions-item>
        <a-descriptions-item label="领域">{{ content.domain }}</a-descriptions-item>
        <a-descriptions-item label="类型">{{ content.content_type }}</a-descriptions-item>
        <a-descriptions-item label="时长">{{ content.duration_minutes }}分钟</a-descriptions-item>
        <a-descriptions-item label="描述" :span="2">{{ content.summary }}</a-descriptions-item>
      </a-descriptions>
      <a-divider />
      <a-button type="primary" @click="markComplete" :loading="completing">标记为已完成</a-button>
    </a-card>
    <a-spin v-else />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getContentDetail, logLearning } from '@/api/learning';
import PageHeader from '@/components/PageHeader.vue';
import { message } from 'ant-design-vue';

const route = useRoute();
const content = ref<any>({});
const completing = ref(false);

onMounted(async () => {
  content.value = (await getContentDetail(route.params.id as string)) || {};
});

const markComplete = async () => {
  completing.value = true;
  try {
    await logLearning({ content_id: route.params.id as string, duration_minutes: content.value.duration_minutes || 30, status: 'completed' });
    message.success('已记录学习完成！');
  } finally { completing.value = false; }
};
</script>
