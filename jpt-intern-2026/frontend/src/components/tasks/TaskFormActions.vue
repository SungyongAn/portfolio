<template>
  <div class="actions">
    <el-button @click="emit('back')">戻る</el-button>

    <el-button
      type="primary"
      :loading="loading"
      :disabled="!canSubmitTask"
      @click="emit('submit')"
    >
      {{ isEdit ? "更新" : "登録" }}
    </el-button>

    <el-button
      v-if="isEdit && canManageTask"
      type="danger"
      :loading="loading"
      @click="emit('delete')"
    >
      削除
    </el-button>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  isEdit: boolean;
  loading: boolean;
  canSubmitTask: boolean;
  canManageTask: boolean;
}>();

const emit = defineEmits<{
  (e: "back"): void;
  (e: "submit"): void;
  (e: "delete"): void;
}>();
</script>

<style scoped>
.actions {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
</style>