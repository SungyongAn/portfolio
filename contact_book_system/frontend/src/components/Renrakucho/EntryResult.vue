<template>
  <div>
    <h4 class="text-success mb-3">
      <i class="fas fa-check-circle me-2"></i>提出完了
    </h4>

    <!-- 提出内容を必要に応じてここに表示可能 -->
    <p><strong>提出日:</strong> {{ entry.submitted_date }}</p>
    <p><strong>体調:</strong> {{ entry.physical_condition }}</p>
    <p><strong>メンタル:</strong> {{ entry.mental_state }}</p>

    <div class="d-flex gap-2 mt-4">
      <button class="btn btn-primary" @click="$emit('new-entry')">
        <i class="fas fa-plus me-2"></i>新しい連絡帳を作成
      </button>

      <button class="btn btn-secondary" @click="$emit('back')">
        <i class="fas fa-arrow-left me-2"></i>メニューに戻る
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "EntryResult",
  props: ["entry"],
  emits: ["new-entry", "back"],
};
</script>
