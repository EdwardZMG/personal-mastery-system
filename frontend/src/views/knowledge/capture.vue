<template>
  <div class="knowledge-capture">
    <PageHeader title="知识捕获" description="快速记录你的灵感和知识" />

    <a-row :gutter="24">
      <a-col :xs="24" :lg="16">
        <a-card :bordered="false">
          <a-form
            :model="formState"
            :rules="rules"
            ref="formRef"
            layout="vertical"
            @finish="handleSubmit"
          >
            <a-form-item label="内容" name="content">
              <a-textarea
                v-model:value="formState.content"
                placeholder="详细描述你的知识或灵感..."
                :rows="10"
                show-count
                :maxlength="5000"
              />
            </a-form-item>

            <a-row :gutter="16">
              <a-col :span="12">
                <a-form-item label="知识领域" name="domain">
                  <a-select v-model:value="formState.domain" placeholder="选择领域">
                    <a-select-option value="AI">AI</a-select-option>
                    <a-select-option value="marketing">营销</a-select-option>
                    <a-select-option value="chinese_classics">国学经典</a-select-option>
                    <a-select-option value="english">英语</a-select-option>
                    <a-select-option value="speaking">演讲</a-select-option>
                    <a-select-option value="general">综合</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item label="来源" name="source">
                  <a-select v-model:value="formState.source" placeholder="选择来源">
                    <a-select-option value="voice_input">语音输入</a-select-option>
                    <a-select-option value="text_input">文字输入</a-select-option>
                    <a-select-option value="crawler">爬虫抓取</a-select-option>
                    <a-select-option value="manual">手动录入</a-select-option>
                  </a-select>
                </a-form-item>
              </a-col>
            </a-row>

            <a-form-item>
              <a-space>
                <a-button type="primary" html-type="submit" :loading="submitting">
                  保存知识
                </a-button>
                <a-button @click="$router.back()">取消</a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </a-card>
      </a-col>

      <a-col :xs="24" :lg="8">
        <a-card title="捕获提示" :bordered="false">
          <a-typography-paragraph>
            <ul>
              <li>标题要简洁明了，概括核心内容</li>
              <li>内容尽量用自己的话重新表述</li>
              <li>添加标签便于后续检索</li>
              <li>选择正确的领域有助于知识分类</li>
              <li>记录来源方便溯源和深入阅读</li>
            </ul>
          </a-typography-paragraph>
        </a-card>

        <a-card title="最近捕获" :bordered="false" class="mt-16">
          <a-list :data-source="recentItems" size="small">
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta :title="item.content?.slice(0, 30) || '未命名'" :description="formatTime(item.created_at)" />
              </a-list-item>
            </template>
          </a-list>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message, type FormInstance } from 'ant-design-vue';
import dayjs from 'dayjs';
import PageHeader from '@/components/PageHeader.vue';
import { createKnowledge, getKnowledgeList, type KnowledgeItem } from '@/api/knowledge';

const router = useRouter();
const formRef = ref<FormInstance>();
const submitting = ref(false);
const recentItems = ref<KnowledgeItem[]>([]);

const formState = reactive({
  content: '',
  domain: undefined as string | undefined,
  source: 'manual' as string,
});

const rules = {
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  domain: [{ required: true, message: '请选择领域', trigger: 'change' }],
};

function formatTime(time: string) {
  return dayjs(time).format('MM-DD HH:mm');
}

async function handleSubmit() {
  submitting.value = true;
  try {
    await createKnowledge({
      content: formState.content,
      domain: formState.domain,
      source: formState.source,
      language: 'zh',
    });
    message.success('知识保存成功');
    router.push('/knowledge');
  } catch {
    message.error('保存失败');
  } finally {
    submitting.value = false;
  }
}

onMounted(async () => {
  try {
    const res = await getKnowledgeList({ limit: 5 });
    const items = Array.isArray(res) ? res : [];
    recentItems.value = items;
  } catch {
    recentItems.value = [];
  }
});
</script>
