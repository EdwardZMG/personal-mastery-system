<template>
  <div class="admin-page">
    <PageHeader title="管理后台" description="系统管理与数据统计" />

    <a-row :gutter="16" class="mb-24">
      <a-col :xs="12" :lg="6">
        <StatCard label="总用户数" :value="systemStats.total_users" color="#1890ff" :icon="UserOutlined" suffix="人" />
      </a-col>
      <a-col :xs="12" :lg="6">
        <StatCard label="知识总量" :value="systemStats.total_insights" color="#52c41a" :icon="BookOutlined" suffix="条" />
      </a-col>
      <a-col :xs="12" :lg="6">
        <StatCard label="学习内容" :value="systemStats.total_content" color="#722ed1" :icon="ReadOutlined" suffix="个" />
      </a-col>
      <a-col :xs="12" :lg="6">
        <StatCard label="打卡次数" :value="systemStats.total_checkins" color="#faad14" :icon="FireOutlined" suffix="次" />
      </a-col>
    </a-row>

    <a-row :gutter="24">
      <a-col :xs="24">
        <a-card title="快捷操作" :bordered="false">
          <a-space>
            <a-button type="primary" @click="$router.push('/admin/content')">内容管理</a-button>
          </a-space>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { UserOutlined, BookOutlined, ReadOutlined, FireOutlined } from '@ant-design/icons-vue';
import PageHeader from '@/components/PageHeader.vue';
import StatCard from '@/components/StatCard.vue';
import { getSystemStats } from '@/api/admin';

const loading = ref(false);

const systemStats = ref({
  total_users: 0,
  total_insights: 0,
  total_content: 0,
  total_checkins: 0,
});

onMounted(async () => {
  loading.value = true;
  try {
    const statsRes = await getSystemStats();
    if (statsRes) systemStats.value = statsRes;
  } catch {
    // keep defaults
  }
  loading.value = false;
});
</script>
