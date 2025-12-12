<template>
  <div class="d-flex justify-content-center mt-4 px-2">
    <div class="w-100" style="max-width: 1200px">
      <!-- ✅ 更新完了後の表示 -->
      <template v-if="updatedAccounts && showResult">
        <div class="alert alert-success mb-4">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h5 class="mb-2">
                <i class="fas fa-check-circle me-2"></i>更新完了
              </h5>
              <p class="mb-0">{{ saveMessage }}</p>
            </div>
            <button
              type="button"
              class="btn-close"
              @click="closeResult"
            ></button>
          </div>
        </div>

        <h6 class="mb-3">更新されたアカウント情報</h6>
        <div class="card">
          <div class="table-responsive">
            <table class="table table-bordered mb-0">
              <thead class="table-light">
                <tr>
                  <th
                    v-for="col in editableColumns.columns"
                    :key="col.key"
                    :style="{ width: col.width }"
                  >
                    {{ col.label }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in updatedAccounts" :key="index">
                  <td v-for="col in editableColumns.columns" :key="col.key">
                    {{ getCellValue(item, col) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="d-flex justify-content-center gap-2 mt-4">
          <button
            type="button"
            class="btn btn-secondary"
            @click.prevent.stop="resetAndBackToResults"
          >
            <i class="fas fa-arrow-left me-2"></i>検索結果に戻る
          </button>
          <button
            type="button"
            class="btn btn-primary"
            @click.prevent.stop="backToSearch"
          >
            <i class="fas fa-search me-2"></i>検索画面に戻る
          </button>
        </div>
      </template>

      <!-- 編集フォーム -->
      <template v-else>
        <h5 class="mb-3 text-primary text-center">
          <i class="fas fa-edit me-2"></i>アカウント情報編集
        </h5>

        <div class="d-flex justify-content-between mb-3">
          <div class="d-flex gap-2">
            <button
              type="button"
              class="btn btn-secondary"
              @click.prevent.stop="backToResults"
            >
              <i class="fas fa-arrow-left me-2"></i>検索結果に戻る
            </button>
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click.prevent.stop="backToSearch"
            >
              <i class="fas fa-search me-2"></i>検索画面に戻る
            </button>
          </div>
          <button
            type="button"
            class="btn btn-primary"
            :disabled="isSaving"
            @click.prevent.stop="saveChanges"
          >
            <span
              v-if="isSaving"
              class="spinner-border spinner-border-sm me-2"
            ></span>
            <i v-else class="fas fa-save me-2"></i>保存
          </button>
        </div>

        <!-- エラー表示 -->
        <div v-if="showResult && !saveSuccess" class="alert alert-danger mb-3">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <i class="fas fa-exclamation-circle me-2"></i>{{ saveMessage }}
            </div>
            <button
              type="button"
              class="btn-close"
              @click="closeResult"
            ></button>
          </div>
        </div>

        <div class="card">
          <div class="table-responsive">
            <table class="table table-bordered table-hover mb-0">
              <thead class="table-light">
                <tr>
                  <th
                    v-for="col in editableColumns.columns"
                    :key="col.key"
                    :style="{ width: col.width }"
                  >
                    {{ col.label }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in accounts" :key="index">
                  <td v-for="col in editableColumns.columns" :key="col.key">
                    <!-- 編集可能フィールド -->
                    <template v-if="col.editable">
                      <select
                        v-if="col.type === 'select'"
                        v-model="item[col.key]"
                        class="form-select form-select-sm"
                      >
                        <option value="">-</option>
                        <option
                          v-for="opt in getSelectOptions(col)"
                          :key="getSelectValue(col, opt)"
                          :value="getSelectValue(col, opt)"
                        >
                          {{ formatSelectOption(col, opt) }}
                        </option>
                      </select>
                      <input
                        v-else
                        v-model="item[col.key]"
                        class="form-control form-control-sm"
                      />
                    </template>

                    <!-- 編集不可フィールド -->
                    <template v-else>
                      {{ getCellValue(item, col) }}
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  name: "AccountUpdateTable",
  props: {
    accounts: {
      type: Array,
      default: () => [],
    },
  },
  setup() {
    const router = useRouter();

    // Vue Router 経由で検索画面へ戻る
    const backToSearch = () => {
      router.push({ name: "account-search" });
    };

    // Vue Router 経由で検索結果画面へ戻る
    const backToResults = () => {
      router.push({ name: "account-search-results" });
    };

    return { backToSearch, backToResults };
  },
  data() {
    return {
      saveMessage: "",
      saveSuccess: null,
      isSaving: false,
      showResult: false,
      updatedAccounts: null,
      gradeOptions: [0, 1, 2, 3],
      classOptions: ["0", "A", "B", "C"],
      statusOptions: ["在校", "休学", "転校", "卒業", "その他"],
      teacherRoles: [
        { code: "grade_leader", name: "学年主任" },
        { code: "homeroom_teacher", name: "担任" },
        { code: "assistant_teacher", name: "副担任" },
        { code: "subject_teacher", name: "教科担当" },
      ],
      subjects: [
        { code: "Japanese", name: "国語" },
        { code: "SocialStudies", name: "社会" },
        { code: "Mathematics", name: "数学" },
        { code: "Science", name: "理科" },
        { code: "Music", name: "音楽" },
        { code: "Art", name: "美術" },
        { code: "PE", name: "保健体育" },
        { code: "TechnologyHomeEconomics", name: "技術・家庭" },
        { code: "English", name: "英語" },
      ],
    };
  },
  computed: {
    editableColumns() {
      // 省略（元のコードを維持）
      // accounts の role に応じて列を返す
      // ...
      return {}; // 元のロジックをそのまま残す
    },
  },
  mounted() {
    // teacher_role / subject をコード化
    this.accounts = this.accounts.map((acc) => {
      const role = this.teacherRoles.find((r) => r.name === acc.teacher_role);
      if (role) acc.teacher_role = role.code;

      const subject = this.subjects.find((s) => s.name === acc.subject);
      if (subject) acc.subject = subject.code;

      return acc;
    });
  },
  methods: {
    saveChanges(event) {
      // 元の saveChanges ロジックを維持
    },
    closeResult() {
      this.showResult = false;
      this.updatedAccounts = null;
    },
    resetAndBackToResults() {
      this.showResult = false;
      this.updatedAccounts = null;
      this.backToResults();
    },
    getCellValue(item, column) {
      // 元の getCellValue ロジックを維持
    },
    getSelectOptions(column) {
      // 元の getSelectOptions ロジックを維持
    },
    formatSelectOption(column, option) {
      // 元の formatSelectOption ロジックを維持
    },
    getSelectValue(column, option) {
      // 元の getSelectValue ロジックを維持
    },
  },
};
</script>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}
</style>
