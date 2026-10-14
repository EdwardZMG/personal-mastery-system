<template>
  <div class="review-session">
    <PageHeader title="复盘会话" :subtitle="session.review_type" />
    <a-card v-if="session.id">
      <a-alert v-if="session.status === 'pending'" message="请回答以下问题" type="info" show-icon style="margin-bottom: 16px" />
      <div v-if="session.questions_json" class="questions">
        <a-form layout="vertical">
          <a-form-item v-for="(q, key) in session.questions_json" :key="key" :label="key">
            <a-textarea v-model:value="answers[key]" :rows="3" :placeholder="q" />
          </a-form-item>
        </a-form>
      </div>
      <a-divider />
      <a-button v-if="session.status === 'pending'" type="primary" @click="submitAnswers" :loading="submitting">提交复盘</a-button>
      <a-descriptions v-if="session.status === 'completed'" :column="1" bordered>
        <a-descriptions-item label="总结">{{ session.summary }}</a-descriptions-item>
        <a-descriptions-item label="回答">{{ session.responses }}</a-descriptions-item>
      </a-descriptions>
    </a-card>
    <a-spin v-else />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getReviewDetail, submitReview } from '@/api/review';
import PageHeader from '@/components/PageHeader.vue';
import { message } from 'ant-design-vue';

const route = useRoute();
const session = ref<any>({});
const answers = ref<Record<string, string>>({});
const submitting = ref(false);

onMounted(async () => {
  session.value = (await getReviewDetail(route.params.id as string)) || {};
});

const submitAnswers = async () => {
  submitting.value = true;
  try {
    const responses = Object.entries(answers.value).map(([k, v]) => `${k}: ${v}`).join('\n');
    await submitReview(route.params.id as string, { responses });
    message.success('复盘已提交！');
    session.value = (await getReviewDetail(route.params.id as string)) || {};
  } finally { submitting.value = false; }
};
</script>
