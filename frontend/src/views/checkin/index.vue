<template>
  <div class="checkin-page">
    <PageHeader title="每日签到" description="记录你今天的成长足迹" />

    <a-row :gutter="24">
      <a-col :xs="24" :lg="14">
        <a-card :bordered="false" title="今日签到" class="mb-24">
          <div class="checkin-status">
            <div v-if="checkedIn" class="checked-in">
              <CheckCircleOutlined class="check-icon success" />
              <h3>今日已签到</h3>
              <p>坚持就是胜利！继续保持！</p>
            </div>
            <div v-else class="not-checked">
              <a-button type="primary" size="large" @click="handleCheckIn" :loading="checking">
                立即签到
              </a-button>
              <p class="mt-16">点击签到，记录今天的成长</p>
            </div>
          </div>
        </a-card>

        <a-card :bordered="false" title="今日反思">
          <a-form layout="vertical">
            <a-form-item label="今天学到了什么？">
              <a-textarea v-model:value="reflection.learned" :rows="3" placeholder="记录今天的新知识或新发现" />
            </a-form-item>
            <a-form-item label="今天有什么做得好的？">
              <a-textarea v-model:value="reflection.good" :rows="2" placeholder="肯定自己的进步和努力" />
            </a-form-item>
            <a-form-item label="明天计划做什么？">
              <a-textarea v-model:value="reflection.plan" :rows="2" placeholder="规划明天的重点任务" />
            </a-form-item>
            <a-form-item>
              <a-button type="primary" @click="saveReflection" :loading="saving">保存反思</a-button>
            </a-form-item>
          </a-form>
        </a-card>
      </a-col>

      <a-col :xs="24" :lg="10">
        <a-card :bordered="false" title="签到日历" class="mb-24">
          <a-calendar v-model:value="currentDate" :fullscreen="false">
            <template #dateCellRender="{ current }">
              <ul class="calendar-events">
                <li v-if="checkedDates.includes(current.format('YYYY-MM-DD'))">
                  <a-badge status="success" />
                </li>
              </ul>
            </template>
          </a-calendar>
        </a-card>

        <a-card :bordered="false" title="签到统计">
          <a-descriptions :column="1">
            <a-descriptions-item label="连续签到">
              <span class="stat-highlight">{{ streakDays }} 天</span>
            </a-descriptions-item>
            <a-descriptions-item label="本月签到">
              <span class="stat-highlight">{{ monthDays }} 天</span>
            </a-descriptions-item>
            <a-descriptions-item label="总签到天数">
              <span class="stat-highlight">{{ totalDays }} 天</span>
            </a-descriptions-item>
          </a-descriptions>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { message } from 'ant-design-vue';
import { CheckCircleOutlined } from '@ant-design/icons-vue';
import dayjs, { Dayjs } from 'dayjs';
import PageHeader from '@/components/PageHeader.vue';
import { getTodayCheckin, listCheckins, createCheckin } from '@/api/checkin';

const checkedIn = ref(false);
const checking = ref(false);
const saving = ref(false);
const streakDays = ref(0);
const monthDays = ref(0);
const totalDays = ref(0);
const currentDate = ref<Dayjs>(dayjs());
const checkedDates = ref<string[]>([]);
const todayCheckin = ref<any>(null);

const reflection = reactive({
  learned: '',
  good: '',
  plan: '',
});

function calcStreak(dates: string[]): number {
  let streak = 0;
  let d = dayjs();
  while (dates.includes(d.format('YYYY-MM-DD'))) {
    streak++;
    d = d.subtract(1, 'day');
  }
  return streak;
}

async function loadData() {
  try {
    const today = await getTodayCheckin();
    checkedIn.value = true;
    todayCheckin.value = today;
    reflection.learned = today.reflections || '';
    reflection.plan = today.tomorrow_plan || '';
  } catch {
    checkedIn.value = false;
  }

  try {
    const monthStart = dayjs().startOf('month').format('YYYY-MM-DD');
    const history = await listCheckins({ start_date: monthStart, limit: 365 });
    const dates = (history as any[]).map((c: any) => c.checkin_date);
    checkedDates.value = dates;
    streakDays.value = calcStreak(dates);
    monthDays.value = dates.filter((d: string) => d.startsWith(dayjs().format('YYYY-MM'))).length;
    totalDays.value = dates.length;
  } catch {
    // silent
  }
}

async function handleCheckIn() {
  checking.value = true;
  try {
    await createCheckin({
      reflections: reflection.learned || undefined,
      tomorrow_plan: reflection.plan || undefined,
    });
    checkedIn.value = true;
    message.success('签到成功！');
    await loadData();
  } catch (e: any) {
    message.error(e?.response?.data?.detail || '签到失败');
  } finally {
    checking.value = false;
  }
}

async function saveReflection() {
  saving.value = true;
  try {
    if (checkedIn.value && todayCheckin.value) {
      message.success('反思已更新');
    } else {
      await createCheckin({
        reflections: reflection.learned || undefined,
        achievements: reflection.good || undefined,
        tomorrow_plan: reflection.plan || undefined,
      });
      checkedIn.value = true;
      message.success('签到并保存反思成功！');
    }
    await loadData();
  } catch (e: any) {
    message.error(e?.response?.data?.detail || '保存失败');
  } finally {
    saving.value = false;
  }
}

onMounted(loadData);
</script>

<style scoped lang="less">
.checkin-status {
  text-align: center;
  padding: 32px 0;

  .check-icon {
    font-size: 64px;

    &.success {
      color: #52c41a;
    }
  }

  h3 {
    margin: 16px 0 8px;
    font-size: 20px;
  }

  p {
    color: rgba(0, 0, 0, 0.45);
  }
}

.calendar-events {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
}

.stat-highlight {
  font-size: 18px;
  font-weight: 700;
  color: #1890ff;
}
</style>
