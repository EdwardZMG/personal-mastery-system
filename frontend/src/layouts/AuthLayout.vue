<template>
  <a-layout class="auth-layout">
    <a-layout-content class="auth-content">
      <div class="auth-container">
        <div class="auth-header">
          <h1 class="auth-title">Edward 个人成长成功系统</h1>
          <p class="auth-subtitle">智慧成长，卓越人生</p>
        </div>
        <router-view />
      </div>
    </a-layout-content>
  </a-layout>
</template>

<script setup lang="ts">
// Auth layout - centered login card
</script>

<style scoped lang="less">
.auth-layout {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-content {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.auth-container {
  width: 100%;
  max-width: 420px;
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-title {
  color: #fff;
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 8px;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.85);
  font-size: 16px;
  margin: 0;
}
</style>
