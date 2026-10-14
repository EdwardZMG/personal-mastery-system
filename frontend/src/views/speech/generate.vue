<template>
  <div class="speech-generate">
    <PageHeader title="生成演讲稿" subtitle="选择模板，输入要点，AI 辅助生成" />
    <a-card>
      <a-form :model="form" layout="vertical" @finish="generate">
        <a-form-item label="演讲主题" name="topic" :rules="[{ required: true }]">
          <a-input v-model:value="form.topic" placeholder="例：AI 时代的领导力" />
        </a-form-item>
        <a-form-item label="模板类型" name="template_type" :rules="[{ required: true }]">
          <a-select v-model:value="form.template_type">
            <a-select-option value="ted_talk">TED Talk (~18分钟)</a-select-option>
            <a-select-option value="toastmasters">Toastmasters (~7分钟)</a-select-option>
            <a-select-option value="elevator_pitch">电梯演讲 (~1分钟)</a-select-option>
            <a-select-option value="storytelling">英雄之旅 (~15分钟)</a-select-option>
          </a-select>
        </a-form-item>
        <a-form-item label="核心要点（每行一个）" name="key_points" :rules="[{ required: true }]">
          <a-textarea v-model:value="keyPointsText" :rows="4" placeholder="要点1&#10;要点2&#10;要点3" />
        </a-form-item>
        <a-form-item label="目标听众">
          <a-input v-model:value="form.audience" placeholder="例：企业管理者、创业者" />
        </a-form-item>
        <a-form-item label="语调">
          <a-select v-model:value="form.tone">
            <a-select-option value="inspirational">激励型</a-select-option>
            <a-select-option value="educational">教育型</a-select-option>
            <a-select-option value="persuasive">说服型</a-select-option>
            <a-select-option value="motivational">动力型</a-select-option>
          </a-select>
        </a-form-item>
        <a-button type="primary" html-type="submit" :loading="generating" size="large">生成演讲稿</a-button>
      </a-form>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { generateSpeech } from '@/api/speech';
import PageHeader from '@/components/PageHeader.vue';
import { message } from 'ant-design-vue';

const router = useRouter();
const generating = ref(false);
const keyPointsText = ref('');
const form = ref({ topic: '', template_type: 'ted_talk', audience: '', tone: 'inspirational' });

const generate = async () => {
  generating.value = true;
  try {
    const key_points = keyPointsText.value.split('\n').filter(Boolean);
    const res = await generateSpeech({ ...form.value, key_points });
    message.success('演讲稿已生成！');
    router.push(`/speech/${res.id}`);
  } finally { generating.value = false; }
};
</script>
