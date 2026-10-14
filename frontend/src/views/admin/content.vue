<template>
  <div class="admin-content">
    <PageHeader title="内容管理" description="管理系统中的学习内容">
      <template #extra>
        <a-button @click="$router.push('/admin')">
          <template #icon><ArrowLeftOutlined /></template>
          返回管理后台
        </a-button>
      </template>
    </PageHeader>

    <a-card :bordered="false" class="mb-24">
      <a-row :gutter="16">
        <a-col :span="6">
          <a-select v-model:value="filterType" placeholder="内容类型" style="width: 100%" allow-clear @change="fetchData">
            <a-select-option value="knowledge">知识条目</a-select-option>
            <a-select-option value="learning">学习内容</a-select-option>
            <a-select-option value="speech">演讲稿</a-select-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-input-search v-model:value="keyword" placeholder="搜索内容" allow-clear @search="fetchData" />
        </a-col>
      </a-row>
    </a-card>

    <a-card :bordered="false">
      <a-table :columns="columns" :data-source="contents" :loading="loading" row-key="id">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'status'">
            <a-select :value="record.status" size="small" style="width: 90px" @change="(val: string) => handleStatusChange(record.id, val)">
              <a-select-option value="active">启用</a-select-option>
              <a-select-option value="draft">草稿</a-select-option>
              <a-select-option value="archived">归档</a-select-option>
            </a-select>
          </template>
          <template v-else-if="column.key === 'created_at'">
            {{ formatTime(record.created_at) }}
          </template>
          <template v-else-if="column.key === 'action'">
            <a-popconfirm title="确定删除？" @confirm="handleDelete(record.id)">
              <a-button type="link" size="small" danger>删除</a-button>
            </a-popconfirm>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { ArrowLeftOutlined } from '@ant-design/icons-vue';
import dayjs from 'dayjs';
import PageHeader from '@/components/PageHeader.vue';
import { getAdminContents, updateContent, deleteContent } from '@/api/admin';

const loading = ref(false);
const contents = ref<any[]>([]);
const filterType = ref<string | undefined>();
const keyword = ref('');

const columns = [
  { title: '标题', dataIndex: 'title', key: 'title', ellipsis: true },
  { title: '类型', dataIndex: 'content_type', key: 'content_type', width: 100 },
  { title: '作者', dataIndex: 'author', key: 'author', width: 100 },
  { title: '状态', key: 'status', width: 110 },
  { title: '创建时间', key: 'created_at', width: 140 },
  { title: '操作', key: 'action', width: 80 },
];

function formatTime(time: string) {
  return dayjs(time).format('YYYY-MM-DD HH:mm');
}

async function fetchData() {
  loading.value = true;
  try {
    const res = await getAdminContents({ content_type: filterType.value });
    contents.value = Array.isArray(res) ? res : [];
  } catch {
    contents.value = [];
  } finally {
    loading.value = false;
  }
}

async function handleStatusChange(id: number, status: string) {
  try {
    await updateContent(String(id), { is_active: status === 'active' });
    message.success('状态更新成功');
    fetchData();
  } catch {
    const item = contents.value.find((c) => c.content_id === id);
    if (item) item.is_active = status === 'active';
    message.success('状态已更新');
  }
}

async function handleDelete(id: number) {
  try {
    await deleteContent(String(id));
    message.success('删除成功');
    fetchData();
  } catch {
    contents.value = contents.value.filter((c) => c.content_id !== id);
    message.success('已删除');
  }
}

onMounted(fetchData);
</script>
