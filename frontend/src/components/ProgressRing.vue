<template>
  <div class="progress-ring">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
      <!-- Background circle -->
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke="trailColor"
        :stroke-width="strokeWidth"
      />
      <!-- Progress circle -->
      <circle
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke="color"
        :stroke-width="strokeWidth"
        :stroke-dasharray="circumference"
        :stroke-dashoffset="dashOffset"
        stroke-linecap="round"
        :transform="`rotate(-90 ${size / 2} ${size / 2})`"
        style="transition: stroke-dashoffset 0.6s ease"
      />
    </svg>
    <div class="progress-ring-text">
      <span class="progress-ring-value">{{ percent }}</span>
      <span class="progress-ring-unit">%</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(defineProps<{
  percent: number;
  size?: number;
  strokeWidth?: number;
  color?: string;
  trailColor?: string;
}>(), {
  size: 120,
  strokeWidth: 8,
  color: '#1890ff',
  trailColor: '#f0f0f0',
});

const radius = computed(() => (props.size - props.strokeWidth) / 2);
const circumference = computed(() => 2 * Math.PI * radius.value);
const dashOffset = computed(() => {
  const pct = Math.min(100, Math.max(0, props.percent));
  return circumference.value * (1 - pct / 100);
});
</script>

<style scoped lang="less">
.progress-ring {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.progress-ring-text {
  position: absolute;
  display: flex;
  align-items: baseline;
  justify-content: center;
}

.progress-ring-value {
  font-size: 24px;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.85);
}

.progress-ring-unit {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
  margin-left: 2px;
}
</style>
