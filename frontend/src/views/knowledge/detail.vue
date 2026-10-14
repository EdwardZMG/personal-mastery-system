<template>
  <div class="knowledge-detail">
    <PageHeader :title="(knowledge.content?.slice(0, 30) || '知识详情')" :description="`领域: ${knowledge.domain}`">
      <template #extra>
        <a-space>
          <a-button @click="$router.back()">
            <template #icon><ArrowLeftOutlined /></template>
            返回
          </a-button>
          <a-button type="primary" @click="showEditModal = true">编辑</a-button>
        </a-space>
      </template>
    </PageHeader>

    <a-spin :spinning="loading">
      <a-row :gutter="24">
        <a-col :xs="24" :lg="16">
          <a-card :bordered="false">
            <a-typography>
              <a-typography-paragraph>
                <div class="detail-meta">
                  <a-tag :color="getDomainColor(knowledge.domain || '')">{{ knowledge.domain }}</a-tag>
                  <a-tag>{{ knowledge.source || knowledge.intent }}</a-tag>
                  <span class="meta-time">创建于 {{ formatTime(knowledge.created_at) }}</span>
                </div>
              </a-typography-paragraph>
              <a-typography-paragraph>
                <div class="detail-content" v-html="formatContent(knowledge.content)"></div>
              </a-typography-paragraph>
            </a-typography>

            <a-divider />

            <div class="detail-tags">
              <strong>标签：</strong>
              <a-tag v-for="tag in knowledge.tags" :key="tag" color="blue">{{ tag }}</a-tag>
              <span v-if="!knowledge.tags?.length" style="color: rgba(0,0,0,.25)">暂无标签</span>
            </div>

            <div v-if="knowledge.source" class="detail-source mt-16">
              <strong>来源：</strong>
              <span>{{ knowledge.source }}</span>
            </div>
          </a-card>
        </a-col>

        <a-col :xs="24" :lg="8">
          <a-card title="关联复习" :bordered="false">
            <a-empty v-if="!relatedReviews.length" description="暂无关联复习" />
            <a-list v-else :data-source="relatedReviews" size="small">
              <template #renderItem="{ item }">
                <a-list-item>
                  <a-list-item-meta :title="item.title" :description="item.date" />
                </a-list-item>
              </template>
            </a-list>
          </a-card>

          <a-card title="知识状态" :bordered="false" class="mt-16">
            <a-descriptions :column="1" size="small">
              <a-descriptions-item label="状态">
                <a-badge :status="knowledge.status === 'structured' ? 'success' : 'default'" :text="statusText" />
              </a-descriptions-item>
              <a-descriptions-item label="创建时间">
                {{ formatTime(knowledge.created_at) }}
              </a-descriptions-item>
            </a-descriptions>
          </a-card>
        </a-col>
      </a-row>
    </a-spin>

    <!-- Edit Modal -->
    <a-modal
      v-model:open="showEditModal"
      title="编辑知识"
      @ok="handleEdit"
      :confirm-loading="editLoading"
      width="640px"
    >
      <a-form layout="vertical">
        <a-form-item label="标题">
          <a-input v-model:value="editForm.title" />
        </a-form-item>
        <a-form-item label="内容">
          <a-textarea v-model:value="editForm.content" :rows="6" />
        </a-form-item>
        <a-form-item label="标签">
          <a-select v-model:value="editForm.tags" mode="tags" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { message } from 'ant-design-vue';
import { ArrowLeftOutlined } from '@ant-design/icons-vue';
import dayjs from 'dayjs';
import PageHeader from '@/components/PageHeader.vue';
import { getKnowledgeDetail, type KnowledgeItem } from '@/api/knowledge';

const route = useRoute();
const loading = ref(true);
const editLoading = ref(false);
const showEditModal = ref(false);

const knowledge = ref<Partial<KnowledgeItem>>({});
const relatedReviews = ref<{ title: string; date: string }[]>([]);

const editForm = reactive({
  title: '',
  content: '',
  tags: [] as string[],
});

const statusText = (() => {
  const map: Record<string, string> = { raw: '原始', structured: '已结构化', archived: '已归档' };
  return map[knowledge.value.status || 'raw'] || '原始';
})();

function getDomainColor(domain: string): string {
  const colors: Record<string, string> = {
    AI: 'blue', marketing: 'green', chinese_classics: 'gold',
    english: 'purple', speaking: 'orange', general: 'default',
  };
  return colors[domain] || 'default';
}

function formatTime(time?: string) {
  return time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '-';
}

function formatContent(content?: string) {
  if (!content) return '';
  return content.replace(/\n/g, '<br>');
}

async function handleEdit() {
  editLoading.value = true;
  try {
    message.info('编辑功能暂未开放');
    showEditModal.value = false;
  } catch {
    message.error('更新失败');
  } finally {
    editLoading.value = false;
  }
}

onMounted(async () => {
  const id = route.params.id as string;
  try {
    knowledge.value = await getKnowledgeDetail(id);
  } catch {
    knowledge.value = {
      id,
      content: '加载失败，请稍后重试',
      domain: 'general',
      tags: [],
      source: 'manual',
      status: 'raw',
      created_at: dayjs().toISOString(),
    };
  }

  editForm.title = (knowledge.value as any).content?.slice(0, 30) || '';
  editForm.content = knowledge.value.content || '';
  editForm.tags = knowledge.value.tags || [];

  relatedReviews.value = [
    { title: '第一次复习', date: dayjs().subtract(1, 'day').format('MM-DD HH:mm') },
    { title: '第二次复习', date: dayjs().subtract(3, 'day').format('MM-DD HH:mm') },
  ];
  loading.value = false;
});
</script>

<style scoped lang="less">
.detail-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;

  .meta-time {
    color: rgba(0, 0, 0, 0.25);
    font-size: 13px;
  }
}

.detail-content {
  font-size: 15px;
  line-height: 1.8;
  color: rgba(0, 0, 0, 0.75);
}

.detail-tags {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.detail-source {
  word-break: break-all;
}
</style>
