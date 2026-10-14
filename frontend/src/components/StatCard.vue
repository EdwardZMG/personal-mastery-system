<template>
  <a-card class="stat-card" :bordered="false" :body-style="{ padding: '20px 24px' }">
    <div class="stat-card-content">
      <div class="stat-info">
        <div class="stat-label">{{ label }}</div>
        <div class="stat-value" :style="{ color: color }">
          <span v-if="prefix" class="stat-prefix">{{ prefix }}</span>
          {{ value }}
          <span v-if="suffix" class="stat-suffix">{{ suffix }}</span>
        </div>
      </div>
      <div v-if="icon" class="stat-icon" :style="{ backgroundColor: color + '15', color }">
        <component :is="icon" />
      </div>
    </div>
    <div v-if="footer" class="stat-footer">
      <slot name="footer">{{ footer }}</slot>
    </div>
  </a-card>
</template>

<script setup lang="ts">
import type { Component } from 'vue';

defineProps<{
  label: string;
  value: string | number;
  color?: string;
  icon?: Component;
  prefix?: string;
  suffix?: string;
  footer?: string;
}>();
</script>

<style scoped lang="less">
.stat-card {
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.3s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
}

.stat-card-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.45);
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
}

.stat-prefix {
  font-size: 16px;
  margin-right: 2px;
}

.stat-suffix {
  font-size: 14px;
  font-weight: 400;
  margin-left: 4px;
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.stat-footer {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.45);
}
</style>
