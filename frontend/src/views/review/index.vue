<template>
  <div class="review-list">
    <PageHeader title="复盘管理" subtitle="定期复盘，持续进化" />
    <a-card>
      <a-button type="primary" @click="triggerReview('daily')" style="margin-bottom: 16px">发起每日复盘</a-button>
      <a-button @click="triggerReview('weekly')" style="margin-left: 8px; margin-bottom: 16px">周复盘</a-button>
      <a-button @click="triggerReview('monthly')" style="margin-left: 8px; margin-bottom: 16px">月复盘</a-button>
      <a-table :columns="columns" :data-source="reviews" :loading="loading" row-key="id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-tag :color="record.status === 'completed' ? 'green' : 'orange'">{{ record.status === 'completed' ? '已完成' : '待完成' }}</a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-button type="link" @click="goSession(record.id)">查看</a-button>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getReviewList, triggerReviewSession } from '@/api/review';
import PageHeader from '@/components/PageHeader.vue';
import { message } from 'ant-design-vue';

const router = useRouter();
const reviews = ref<any[]>([]);
const loading = ref(false);
const columns = [
  { title: '类型', dataIndex: 'review_type', key: 'review_type' },
  { title: '计划时间', dataIndex: 'scheduled_time', key: 'scheduled_time' },
  { title: '状态', key: 'status' },
  { title: '操作', key: 'action' },
];

const loadReviews = async () => {
  loading.value = true;
  try { const res = await getReviewList(); reviews.value = Array.isArray(res) ? res : []; }
  finally { loading.value = false; }
};

const triggerReview = async (type: string) => {
  await triggerReviewSession({ review_type: type });
  message.success(`${type} 复盘已发起`);
  await loadReviews();
};

const goSession = (id: string) => router.push(`/review/${id}`);

onMounted(loadReviews);
</script>
