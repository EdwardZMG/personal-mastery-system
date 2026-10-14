<template>
  <div class="speech-detail">
    <PageHeader :title="speech.topic || '演讲详情'" :subtitle="speech.template_type" />
    <a-card v-if="speech.id">
      <a-descriptions :column="2" bordered>
        <a-descriptions-item label="主题">{{ speech.topic }}</a-descriptions-item>
        <a-descriptions-item label="时长">{{ speech.estimated_duration }} 分钟</a-descriptions-item>
        <a-descriptions-item label="状态">{{ speech.status }}</a-descriptions-item>
        <a-descriptions-item label="创建时间">{{ speech.created_at }}</a-descriptions-item>
      </a-descriptions>
      <a-divider>演讲全文</a-divider>
      <div class="speech-content" v-if="speech.full_speech">{{ speech.full_speech }}</div>
      <a-empty v-else description="演讲内容待生成" />
      <a-divider v-if="speech.speaker_notes">演讲备注</a-divider>
      <div class="notes" v-if="speech.speaker_notes" style="white-space: pre-wrap; color: #666;">{{ speech.speaker_notes }}</div>
    </a-card>
    <a-spin v-else />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { getSpeechDetail } from '@/api/speech';
import PageHeader from '@/components/PageHeader.vue';

const route = useRoute();
const speech = ref<any>({});

onMounted(async () => {
  speech.value = (await getSpeechDetail(route.params.id as string)) || {};
});
</script>

<style scoped>
.speech-content { white-space: pre-wrap; line-height: 1.8; font-size: 15px; }
</style>
