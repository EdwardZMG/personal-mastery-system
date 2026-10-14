<template>
  <div class="speech-list">
    <PageHeader title="演讲稿" subtitle="TED / Toastmasters / 电梯演讲 / 故事讲述" />
    <a-card>
      <a-button type="primary" @click="$router.push('/speech/generate')" style="margin-bottom: 16px">生成新演讲</a-button>
      <a-table :columns="columns" :data-source="speeches" :loading="loading" row-key="id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'template_type'">
            <a-tag color="blue">{{ templateLabel(record.template_type) }}</a-tag>
          </template>
          <template v-if="column.key === 'status'">
            <a-tag :color="record.status === 'delivered' ? 'green' : record.status === 'draft' ? 'default' : 'orange'">{{ record.status }}</a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-button type="link" @click="$router.push(`/speech/${record.id}`)">查看</a-button>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getSpeechList } from '@/api/speech';
import PageHeader from '@/components/PageHeader.vue';

const speeches = ref<any[]>([]);
const loading = ref(false);
const columns = [
  { title: '主题', dataIndex: 'topic', key: 'topic' },
  { title: '模板', key: 'template_type' },
  { title: '时长(分钟)', dataIndex: 'estimated_duration', key: 'estimated_duration' },
  { title: '状态', key: 'status' },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  { title: '操作', key: 'action' },
];
const templateLabel = (t: string) => ({ ted_talk: 'TED Talk', toastmasters: 'Toastmasters', elevator_pitch: '电梯演讲', storytelling: '故事讲述' }[t] || t);

onMounted(async () => {
  loading.value = true;
  try { const res = await getSpeechList(); speeches.value = Array.isArray(res) ? res : []; }
  finally { loading.value = false; }
});
</script>
