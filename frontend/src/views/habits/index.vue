<template>
  <div class="habits-page">
    <PageHeader title="习惯追踪" subtitle="6大核心习惯养成" />
    <a-row :gutter="16">
      <a-col :span="8" v-for="habit in habits" :key="habit.id">
        <a-card>
          <template #title>{{ habit.name }}</template>
          <template #extra><a-tag color="green">连续 {{ habit.current_streak }} 天</a-tag></template>
          <p>{{ habit.description }}</p>
          <p>频率: {{ habit.frequency }} | 总完成: {{ habit.total_completions }}</p>
          <a-button type="primary" block @click="logHabit(habit.id)" :loading="loggingId === habit.id">今日打卡</a-button>
        </a-card>
      </a-col>
    </a-row>
    <a-empty v-if="habits.length === 0" description="暂无习惯，点击下方创建">
      <a-button type="primary" @click="showModal = true">创建习惯</a-button>
    </a-empty>
    <a-modal v-model:open="showModal" title="创建习惯" @ok="createHabit">
      <a-form layout="vertical">
        <a-form-item label="习惯名称"><a-input v-model:value="form.name" /></a-form-item>
        <a-form-item label="描述"><a-input v-model:value="form.description" /></a-form-item>
        <a-form-item label="频率">
          <a-select v-model:value="form.frequency">
            <a-select-option value="daily">每日</a-select-option>
            <a-select-option value="weekly">每周</a-select-option>
          </a-select>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getHabits, createHabit as apiCreate, logHabit as apiLog } from '@/api/habits';
import PageHeader from '@/components/PageHeader.vue';
import { message } from 'ant-design-vue';

const habits = ref<any[]>([]);
const showModal = ref(false);
const loggingId = ref<string | null>(null);
const form = ref({ name: '', description: '', frequency: 'daily' });

const load = async () => { const res = await getHabits(); habits.value = Array.isArray(res) ? res : []; };
const createHabit = async () => { await apiCreate(form.value); message.success('习惯已创建'); showModal.value = false; await load(); };
const logHabit = async (id: string) => { loggingId.value = id; try { await apiLog(id, { count: 1, note: '每日打卡' }); message.success('打卡成功！'); await load(); } finally { loggingId.value = null; } };
onMounted(load);
</script>
