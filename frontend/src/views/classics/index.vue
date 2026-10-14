<template>
  <div class="classics-page">
    <PageHeader title="国学经典" subtitle="道德经 · 金刚经 · 六祖坛经 · 资治通鉴 · 易经 · 孙子兵法" />
    <a-row :gutter="16">
      <a-col :span="8" v-for="book in books" :key="book.name">
        <a-card hoverable @click="$router.push(`/classics/${book.name}`)">
          <template #title>{{ book.name }}</template>
          <a-progress :percent="Math.round((book.mastery || 0) * 100)" :stroke-color="'#cf1322'" />
          <p style="color:#999; margin-top:8px">{{ book.chapters_completed || 0 }} / {{ book.total_chapters }} 章</p>
          <a-tag color="red">{{ book.status || '未开始' }}</a-tag>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getAllClassicsProgress } from '@/api/classics';
import PageHeader from '@/components/PageHeader.vue';

const books = ref([
  { name: '道德经', mastery: 0, chapters_completed: 0, total_chapters: 81, status: '未开始' },
  { name: '金刚经', mastery: 0, chapters_completed: 0, total_chapters: 32, status: '未开始' },
  { name: '六祖坛经', mastery: 0, chapters_completed: 0, total_chapters: 10, status: '未开始' },
  { name: '资治通鉴', mastery: 0, chapters_completed: 0, total_chapters: 294, status: '未开始' },
  { name: '易经', mastery: 0, chapters_completed: 0, total_chapters: 64, status: '未开始' },
  { name: '孙子兵法', mastery: 0, chapters_completed: 0, total_chapters: 13, status: '未开始' },
]);

onMounted(async () => {
  try {
    const res = await getAllClassicsProgress();
    const data = Array.isArray(res) ? res : [];
    data.forEach((item: any) => {
      const book = books.value.find(b => b.name === item.classic_name);
      if (book) { book.mastery = item.mastery_level; book.status = item.status; }
    });
  } catch { /* use defaults */ }
});
</script>
