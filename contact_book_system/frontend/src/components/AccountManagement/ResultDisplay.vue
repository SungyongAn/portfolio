<template>
  <div
    v-if="show"
    class="mt-4 alert"
    :class="alertClass"
    role="alert"
    style="border: 2px solid currentColor"
  >
    <div class="d-flex justify-content-between align-items-start">
      <h5 class="mb-3">
        <i class="fas" :class="iconClass + ' me-2'"></i>{{ title }}
      </h5>
      <button
        type="button"
        class="btn-close"
        @click="closeResult"
        aria-label="閉じる"
      ></button>
    </div>

    <!-- メッセージがある場合 -->
    <p v-if="message" class="mb-3">{{ message }}</p>

    <!-- データ表示 -->
    <div v-if="displayData.length > 0">
      <!-- 複数件の場合はテーブル表示 -->
      <div v-if="displayData.length > 1" class="table-responsive">
        <table class="table table-sm table-bordered bg-white">
          <thead>
            <tr>
              <th v-for="field in fields" :key="field.key">
                {{ field.label }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in displayData" :key="index">
              <td v-for="field in fields" :key="field.key">
                {{ formatValue(item, field) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 1件の場合はリスト表示 -->
      <div v-else class="result-list bg-white p-3 rounded">
        <div v-for="field in fields" :key="field.key" class="mb-2">
          <strong>{{ field.label }}:</strong>
          {{ formatValue(displayData[0], field) }}
        </div>
      </div>
    </div>

    <!-- 下部ボタン -->
    <div class="mt-3 text-end d-flex justify-content-end gap-2">
      <button
        type="button"
        class="btn btn-secondary"
        @click="closeResult"
      >
        <i class="fas fa-times me-2"></i>閉じる
      </button>

      <button
        v-if="goToSearch"
        type="button"
        class="btn btn-primary"
        @click="navigateToSearch"
      >
        <i class="fas fa-search me-2"></i>検索画面へ
      </button>

      <button
        v-if="goToResults"
        type="button"
        class="btn btn-outline-primary"
        @click="navigateToResults"
      >
        <i class="fas fa-arrow-left me-2"></i>検索結果へ
      </button>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "ResultDisplay",
  props: {
    show: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      default: "success",
      validator: (value) =>
        ["success", "error", "warning", "info"].includes(value),
    },
    title: {
      type: String,
      default: "処理完了",
    },
    data: {
      type: [Object, Array],
      default: null,
    },
    fields: {
      type: Array,
      default: () => [],
    },
    message: {
      type: String,
      default: "",
    },
    // ページ移動ボタン表示制御
    goToSearch: {
      type: Boolean,
      default: false,
    },
    goToResults: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close"],
  setup() {
    const router = useRouter();

    const navigateToSearch = () => {
      router.push({ name: "account-search" });
    };

    const navigateToResults = () => {
      router.push({ name: "account-search-results" });
    };

    return { navigateToSearch, navigateToResults };
  },
  computed: {
    alertClass() {
      const classMap = {
        success: "alert-success",
        error: "alert-danger",
        warning: "alert-warning",
        info: "alert-info",
      };
      return classMap[this.type] || "alert-success";
    },
    iconClass() {
      const iconMap = {
        success: "fa-check-circle",
        error: "fa-exclamation-circle",
        warning: "fa-exclamation-triangle",
        info: "fa-info-circle",
      };
      return iconMap[this.type] || "fa-check-circle";
    },
    displayData() {
      if (!this.data) return [];
      return Array.isArray(this.data) ? this.data : [this.data];
    },
  },
  watch: {
    show(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          const element = this.$el;
          if (element && element.scrollIntoView) {
            element.scrollIntoView({ behavior: "smooth", block: "nearest" });
          }
        });
      }
    },
  },
  methods: {
    closeResult() {
      this.$emit("close");
    },
    formatValue(item, field) {
      let value = item[field.key];

      if (value === null || value === undefined) return "-";

      if (field.formatter && typeof field.formatter === "function") {
        return field.formatter(value, item);
      }

      const prefix = field.prefix || "";
      const suffix = field.suffix || "";

      return `${prefix}${value}${suffix}`;
    },
  },
};
</script>

<style scoped>
.result-list {
  line-height: 1.8;
}
</style>
