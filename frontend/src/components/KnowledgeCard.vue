<template>
  <a-card
    class="knowledge-card"
    hoverable
    :bordered="false"
    @click="$router.push(`/knowledge/${item.id}`)"
  >
    <template #actions>
      <EditOutlined @click.stop="$emit('edit', item)" />
      <DeleteOutlined @click.stop="$emit('delete', item)" />
    </template>
    <a-card-meta :title="item.content?.slice(0, 30) || '未命名'" :description="item.content?.substring(0, 80) + '...'">
      <template #avatar>
        <a-tag :color="domainColor">{{ item.domain }}</a-tag>
      </template>
    </a-card-meta>
    <div class="card-footer">
      <div class="card-tags">
        <a-tag v-for="tag in item.tags?.slice(0, 3)" :key="tag" size="small">{{ tag }}</a-tag>
      </div>
      <span class="card-time">{{ formatTime(item.created_at) }}</span>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons-vue';
import dayjs from 'dayjs';
import type { KnowledgeItem } from '@/api/knowledge';

const props = defineProps<{
  item: KnowledgeItem;
}>();

defineEmits<{
  edit: [item: KnowledgeItem];
  delete: [item: KnowledgeItem];
}>();

const domainColor = computed(() => {
  const colors: Record<string, string> = {
    '哲学': 'purple',
    '科学': 'blue',
    '技术': 'cyan',
    '管理': 'green',
    '心理': 'orange',
    '历史': 'red',
  };
  return colors[props.item.domain] || 'default';
});

function formatTime(time: string) {
  return dayjs(time).format('MM-DD HH:mm');
}
</script>

<style scoped lang="less">
.knowledge-card {
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
}

.card-tags {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.card-time {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.25);
}
</style>
