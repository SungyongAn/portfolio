<template>
  <el-drawer
    v-model="visible"
    title="案件申請"
    direction="rtl"
    size="720px"
    destroy-on-close
  >
    <ProjectCreateForm
      embedded
      @created="handleCreated"
      @cancel="visible = false"
    />
  </el-drawer>
</template>

<script setup lang="ts">
import { computed } from "vue";

import ProjectCreateForm from "@/components/projects/ProjectCreateForm.vue";

const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: "update:modelValue", value: boolean): void;
  (e: "created"): void;
}>();

const visible = computed({
  get: () => props.modelValue,
  set: (value: boolean) => emit("update:modelValue", value),
});

const handleCreated = () => {
  emit("created");
  visible.value = false;
};
</script>
