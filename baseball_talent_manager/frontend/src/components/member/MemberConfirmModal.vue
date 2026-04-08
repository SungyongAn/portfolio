<template>
  <div
    v-if="show"
    class="modal d-block"
    tabindex="-1"
    style="background-color: rgba(0, 0, 0, 0.5)"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">処理の確認</h5>
        </div>

        <div class="modal-body">
          <p>
            <strong>{{ member?.name }}</strong
            >さんを
            <strong
              :class="actionType === 'retired' ? 'text-warning' : 'text-danger'"
            >
              {{ actionType === "retired" ? "引退" : "退部" }}
            </strong>
            として処理します。よろしいですか？
          </p>
        </div>

        <div class="modal-footer">
          <button class="btn btn-outline-secondary" @click="$emit('close')">
            キャンセル
          </button>

          <button
            :class="
              actionType === 'retired' ? 'btn btn-warning' : 'btn btn-danger'
            "
            @click="$emit('confirm')"
          >
            {{ actionType === "retired" ? "引退処理" : "退部処理" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  member: Object,
  actionType: String,
});

defineEmits(["close", "confirm"]);
</script>
