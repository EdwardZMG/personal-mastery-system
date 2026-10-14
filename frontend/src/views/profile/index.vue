<template>
  <div class="profile-page">
    <PageHeader title="个人中心" description="管理个人信息与能力评估" />

    <a-row :gutter="24">
      <a-col :xs="24" :lg="8">
        <a-card :bordered="false" class="mb-24">
          <div class="profile-avatar">
            <a-avatar :size="80" style="background-color: #1890ff; font-size: 32px">
              {{ userInfo.username?.charAt(0)?.toUpperCase() || 'U' }}
            </a-avatar>
            <h3 class="mt-16">{{ userInfo.username || '用户' }}</h3>
            <p style="color: rgba(0,0,0,.45)">{{ userInfo.email || '未设置邮箱' }}</p>
          </div>
          <a-divider />
          <a-descriptions :column="1" size="small">
            <a-descriptions-item label="注册时间">{{ userInfo.created_at || '-' }}</a-descriptions-item>
            <a-descriptions-item label="用户ID">{{ userInfo.id || '-' }}</a-descriptions-item>
          </a-descriptions>
        </a-card>

        <a-card title="基本信息" :bordered="false">
          <a-form layout="vertical">
            <a-form-item label="用户名">
              <a-input v-model:value="editForm.username" />
            </a-form-item>
            <a-form-item label="邮箱">
              <a-input v-model:value="editForm.email" />
            </a-form-item>
            <a-form-item>
              <a-button type="primary" @click="saveProfile" :loading="saving">保存修改</a-button>
            </a-form-item>
          </a-form>
        </a-card>
      </a-col>

      <a-col :xs="24" :lg="16">
        <!-- MASK Scores -->
        <a-card title="MASK 能力评估" :bordered="false" class="mb-24">
          <a-row :gutter="16">
            <a-col :span="12">
              <v-chart :option="maskRadarOption" style="height: 300px" autoresize />
            </a-col>
            <a-col :span="12">
              <div class="mask-scores">
                <div v-for="(score, key) in maskScores" :key="key" class="mask-item">
                  <div class="mask-label">
                    <span>{{ maskLabels[key as string] || key }}</span>
                    <span class="mask-value">{{ score }}</span>
                  </div>
                  <a-progress :percent="score" :show-info="false" :stroke-color="getMaskColor(score)" />
                </div>
              </div>
            </a-col>
          </a-row>
        </a-card>

        <!-- Maslow Scores -->
        <a-card title="马斯洛需求层次评估" :bordered="false">
          <div class="maslow-pyramid">
            <div v-for="(level, idx) in maslowLevels" :key="idx" class="maslow-level" :style="{ width: `${(idx + 1) * 20}%` }">
              <div class="level-info">
                <span class="level-name">{{ level.name }}</span>
                <a-progress :percent="level.score" size="small" :stroke-color="getMaslowColor(idx)" style="width: 120px" />
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { message } from 'ant-design-vue';
import VChart from 'vue-echarts';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { RadarChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, RadarComponent } from 'echarts/components';
import { useUserStore } from '@/store/user';
import { updateProfile } from '@/api/auth';
import PageHeader from '@/components/PageHeader.vue';

use([CanvasRenderer, RadarChart, TitleComponent, TooltipComponent, LegendComponent, RadarComponent]);

const userStore = useUserStore();
const saving = ref(false);

const userInfo = computed(() => userStore.userInfo || {} as any);
const editForm = reactive({ username: '', email: '' });

const maskLabels: Record<string, string> = {
  mindset: '思维模式 (Mindset)',
  attitude: '人生态度 (Attitude)',
  skills: '技能 (Skills)',
  knowledge: '知识储备 (Knowledge)',
};

const maskScores = reactive<Record<string, number>>({
  mindset: 78,
  attitude: 65,
  skills: 72,
  knowledge: 85,
});

const maslowLevels = reactive([
  { name: '生理需求', score: 90 },
  { name: '安全需求', score: 80 },
  { name: '社交需求', score: 72 },
  { name: '尊重需求', score: 65 },
  { name: '自我实现', score: 58 },
]);

const maskRadarOption = computed(() => ({
  tooltip: {},
  radar: {
    indicator: Object.keys(maskScores).map((k) => ({ name: maskLabels[k] || k, max: 100 })),
    shape: 'polygon',
    splitArea: { areaStyle: { color: ['#fff', '#f5f5f5'] } },
  },
  series: [{
    type: 'radar',
    data: [{
      value: Object.values(maskScores),
      name: 'MASK 能力',
      areaStyle: { color: 'rgba(24, 144, 255, 0.2)' },
      lineStyle: { color: '#1890ff' },
    }],
  }],
}));

function getMaskColor(score: number): string {
  if (score >= 80) return '#52c41a';
  if (score >= 60) return '#1890ff';
  if (score >= 40) return '#faad14';
  return '#f5222d';
}

function getMaslowColor(idx: number): string {
  const colors = ['#52c41a', '#1890ff', '#722ed1', '#fa8c16', '#eb2f96'];
  return colors[idx] || '#1890ff';
}

async function saveProfile() {
  saving.value = true;
  try {
    await updateProfile({ username: editForm.username, email: editForm.email });
    message.success('保存成功');
    if (userStore.userInfo) {
      userStore.userInfo.username = editForm.username;
      userStore.userInfo.email = editForm.email;
    }
  } catch {
    message.error('保存失败');
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  editForm.username = userInfo.value.username || '';
  editForm.email = userInfo.value.email || '';
});
</script>

<style scoped lang="less">
.profile-avatar {
  text-align: center;
  padding: 16px 0;
}

.mask-scores {
  .mask-item {
    margin-bottom: 16px;
  }

  .mask-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 14px;
  }

  .mask-value {
    font-weight: 700;
  }
}

.maslow-pyramid {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px 0;

  .maslow-level {
    background: #f5f5f5;
    border-radius: 4px;
    padding: 12px 16px;
    transition: all 0.3s;

    &:hover {
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
  }

  .level-info {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .level-name {
    font-weight: 600;
    font-size: 14px;
  }
}
</style>
