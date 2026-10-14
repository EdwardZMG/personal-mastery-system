<template>
  <div class="goals-page">
    <PageHeader title="目标管理" subtitle="SMART 原则目标设定与追踪" />
    <a-card>
      <a-button type="primary" @click="showModal = true" style="margin-bottom: 16px">新建目标</a-button>
      <a-table :columns="columns" :data-source="goals" :loading="loading" row-key="id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'progress'">
            <a-progress :percent="record.progress_percent || 0" size="small" />
          </template>
          <template v-if="column.key === 'status'">
            <a-tag :color="record.status === 'completed' ? 'green' : 'blue'">{{ record.status === 'completed' ? '已完成' : '进行中' }}</a-tag>
          </template>
          <template v-if="column.key === 'action'">
            <a-button type="link" size="small" @click="editGoal(record)">编辑</a-button>
            <a-popconfirm title="确定删除？" @confirm="deleteGoal(record.id)"><a-button type="link" danger size="small">删除</a-button></a-popconfirm>
          </template>
        </template>
      </a-table>
    </a-card>
    <a-modal v-model:open="showModal" :title="editingId ? '编辑目标' : '新建目标'" @ok="saveGoal" :confirm-loading="saving">
      <a-form layout="vertical">
        <a-form-item label="目标标题"><a-input v-model:value="form.title" /></a-form-item>
        <a-form-item label="描述"><a-textarea v-model:value="form.description" :rows="3" /></a-form-item>
        <a-form-item label="截止日期"><a-date-picker v-model:value="form.deadline" style="width:100%" /></a-form-item>
        <a-form-item label="优先级">
          <a-select v-model:value="form.priority">
            <a-select-option :value="1">高</a-select-option>
            <a-select-option :value="2">中</a-select-option>
            <a-select-option :value="3">低</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="类别"><a-input v-model:value="form.category" placeholder="例：AI学习/营销/国学" /></a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getGoals, createGoal as apiCreate, updateGoal as apiUpdate, deleteGoal as apiDelete } from '@/api/goals';
import PageHeader from '@/components/PageHeader.vue';
import { message } from 'ant-design-vue';

const goals = ref<any[]>([]);
const loading = ref(false);
const showModal = ref(false);
const saving = ref(false);
const editingId = ref<string | null>(null);
const form = ref({ title: '', description: '', deadline: undefined as string | undefined, priority: 2, category: '' });
const columns = [
  { title: '目标', dataIndex: 'title', key: 'title' },
  { title: '类别', dataIndex: 'category', key: 'category' },
  { title: '进度', key: 'progress' },
  { title: '截止日期', dataIndex: 'deadline', key: 'deadline' },
  { title: '状态', key: 'status' },
  { title: '操作', key: 'action' },
];

const load = async () => { loading.value = true; try { const res = await getGoals(); goals.value = Array.isArray(res) ? res : []; } finally { loading.value = false; } };
const saveGoal = async () => { saving.value = true; try { if (editingId.value) { await apiUpdate(editingId.value, form.value); message.success('目标已更新'); } else { await apiCreate(form.value); message.success('目标已创建'); } showModal.value = false; editingId.value = null; form.value = { title: '', description: '', deadline: undefined, priority: 2, category: '' }; await load(); } finally { saving.value = false; } };
const deleteGoal = async (id: string) => { await apiDelete(id); message.success('已删除'); await load(); };
const editGoal = (g: any) => { editingId.value = g.id; form.value = { title: g.title || '', description: g.description || '', deadline: g.deadline || undefined, priority: g.priority || 2, category: g.category || '' }; showModal.value = true; };
onMounted(load);
</script>
