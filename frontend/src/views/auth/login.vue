<template>
  <a-card class="login-card" :bordered="false">
    <a-form
      :model="formState"
      :rules="rules"
      ref="formRef"
      @finish="handleLogin"
      layout="vertical"
    >
      <a-form-item label="Open ID" name="open_id">
        <a-input
          v-model:value="formState.open_id"
          size="large"
          placeholder="请输入您的 Open ID（例：ou_xxxxxxxx）"
        >
          <template #prefix><UserOutlined style="color: rgba(0,0,0,.25)" /></template>
        </a-input>
      </a-form-item>
      <a-form-item>
        <a-button
          type="primary"
          html-type="submit"
          size="large"
          block
          :loading="loading"
        >
          登录
        </a-button>
      </a-form-item>
    </a-form>
  </a-card>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { message, type FormInstance } from 'ant-design-vue';
import { UserOutlined } from '@ant-design/icons-vue';
import { useUserStore } from '@/store/user';

const router = useRouter();
const userStore = useUserStore();
const formRef = ref<FormInstance>();
const loading = ref(false);

const formState = reactive({
  open_id: '',
});

const rules = {
  open_id: [{ required: true, message: '请输入 Open ID', trigger: 'blur' }],
};

async function handleLogin() {
  loading.value = true;
  try {
    await userStore.login(formState.open_id);
    message.success('登录成功');
    router.push('/dashboard');
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '登录失败，请检查 Open ID');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped lang="less">
.login-card {
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}
</style>
