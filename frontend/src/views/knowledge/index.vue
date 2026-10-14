<template>
  <div class="knowledge-list">
    <PageHeader title="知识管理" description="管理和组织你的知识条目">
      <template #extra>
        <a-button type="primary" @click="$router.push('/knowledge/capture')">
          <template #icon><PlusOutlined /></template>
          知识捕获
        </a-button>
      </template>
    </PageHeader>

    <!-- Search & Filter -->
    <a-card :bordered="false" class="mb-24">
      <a-row :gutter="16">
        <a-col :span="8">
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索知识标题或内容"
            allow-clear
            @search="handleSearch"
          />
        </a-col>
        <a-col :span="6">
          <a-select
            v-model:value="filterDomain"
            placeholder="选择领域"
            style="width: 100%"
            allow-clear
            @change="handleSearch"
          >
            <a-select-option value="AI">AI</a-select-option>
            <a-select-option value="marketing">营销</a-select-option>
            <a-select-option value="chinese_classics">国学经典</a-select-option>
            <a-select-option value="english">英语</a-select-option>
            <a-select-option value="speaking">演讲</a-select-option>
            <a-select-option value="general">综合</a-select-option>
          </a-select>
        </a-col>
        <a-col :span="6">
          <a-select
            v-model:value="filterStatus"
            placeholder="选择状态"
            style="width: 100%"
            allow-clear
            @change="handleSearch"
          >
            <a-select-option value="raw">原始</a-select-option>
            <a-select-option value="structured">已结构化</a-select-option>
            <a-select-option value="archived">已归档</a-select-option>
          </a-select>
        </a-col>
      </a-row>
    </a-card>

    <!-- Table -->
    <a-card :bordered="false">
      <a-table
        :columns="columns"
        :data-source="dataList"
        :loading="loading"
        :pagination="pagination"
        row-key="id"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'title'">
            <a @click="$router.push(`/knowledge/${record.id}`)">{{ record.content?.slice(0, 50) || '未命名' }}</a>
          </template>
          <template v-else-if="column.key === 'domain'">
            <a-tag :color="getDomainColor(record.domain)">{{ record.domain }}</a-tag>
          </template>
          <template v-else-if="column.key === 'tags'">
            <a-tag v-for="tag in record.tags?.slice(0, 3)" :key="tag">{{ tag }}</a-tag>
          </template>
          <template v-else-if="column.key === 'status'">
            <a-badge :status="getStatusBadge(record.status)" :text="getStatusText(record.status)" />
          </template>
          <template v-else-if="column.key === 'created_at'">
            {{ formatTime(record.created_at) }}
          </template>
          <template v-else-if="column.key === 'action'">
            <a-button type="link" size="small" @click="$router.push(`/knowledge/${record.id}`)">查看</a-button>
          </template>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import { PlusOutlined } from '@ant-design/icons-vue';
import dayjs from 'dayjs';
import PageHeader from '@/components/PageHeader.vue';
import { getKnowledgeList, type KnowledgeItem } from '@/api/knowledge';

const loading = ref(false);
const dataList = ref<KnowledgeItem[]>([]);
const searchKeyword = ref('');
const filterDomain = ref<string | undefined>();
const filterStatus = ref<string | undefined>();

const pagination = reactive({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条`,
});

const columns = [
  { title: '内容', key: 'title', dataIndex: 'content', ellipsis: true },
  { title: '领域', key: 'domain', dataIndex: 'domain', width: 120 },
  { title: '标签', key: 'tags', dataIndex: 'tags', width: 200 },
  { title: '状态', key: 'status', dataIndex: 'status', width: 100 },
  { title: '创建时间', key: 'created_at', dataIndex: 'created_at', width: 160 },
  { title: '操作', key: 'action', width: 100 },
];

function getDomainColor(domain: string): string {
  const colors: Record<string, string> = {
    AI: 'blue', marketing: 'green', chinese_classics: 'gold',
    english: 'purple', speaking: 'orange', general: 'default',
  };
  return colors[domain] || 'default';
}

function getStatusBadge(status: string): 'default' | 'processing' | 'success' | 'warning' {
  const map: Record<string, 'default' | 'processing' | 'success' | 'warning'> = {
    raw: 'default', structured: 'success', archived: 'warning',
  };
  return map[status] || 'default';
}

function getStatusText(status: string): string {
  const map: Record<string, string> = { raw: '原始', structured: '已结构化', archived: '已归档' };
  return map[status] || status;
}

function formatTime(time: string) {
  return dayjs(time).format('YYYY-MM-DD HH:mm');
}

async function fetchData() {
  loading.value = true;
  try {
    const res = await getKnowledgeList({
      limit: pagination.pageSize,
      offset: (pagination.current - 1) * pagination.pageSize,
      domain: filterDomain.value || undefined,
      status_filter: filterStatus.value || undefined,
    });
    const items = Array.isArray(res) ? res : [];
    dataList.value = items;
    pagination.total = items.length;
  } catch {
    dataList.value = [];
    pagination.total = 0;
  } finally {
    loading.value = false;
  }
}

function handleSearch() {
  pagination.current = 1;
  fetchData();
}

function handleTableChange(pag: any) {
  pagination.current = pag.current;
  pagination.pageSize = pag.pageSize;
  fetchData();
}

onMounted(fetchData);
</script>
