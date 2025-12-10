const AccountUpdateTable = {
  props: {
    accounts: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["back-to-search", "back-to-results"],
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
      // ✅ マスターデータ（AccountFormと同じ）
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
    // ✅ 役割に応じた編集可能列を決定
    editableColumns() {
      if (this.accounts.length === 0) return {};

      const roles = [...new Set(this.accounts.map((a) => a.role))];

      if (roles.length === 1) {
        const role = roles[0];

        if (role === "教師") {
          return {
            columns: [
              { key: "id", label: "ID", editable: false, width: "60px" },
              {
                key: "fullName",
                label: "氏名",
                editable: false,
                width: "120px",
              },
              { key: "role", label: "役割", editable: false, width: "80px" },
              {
                key: "enrollmentYear",
                label: "登録年",
                editable: false,
                width: "90px",
                suffix: "年",
              },
              {
                key: "teacher_role",
                label: "教員区分",
                editable: true,
                width: "130px",
                type: "select",
                options: "teacherRoles",
              },
              {
                key: "subject",
                label: "担当科目",
                editable: true,
                width: "140px",
                type: "select",
                options: "subjects",
              },
              {
                key: "grade",
                label: "学年",
                editable: true,
                width: "90px",
                type: "select",
                suffix: "年",
              },
              {
                key: "className",
                label: "クラス",
                editable: true,
                width: "90px",
                type: "select",
                suffix: "組",
              },
              {
                key: "status",
                label: "状態",
                editable: true,
                width: "110px",
                type: "select",
              },
            ],
          };
        } else if (role === "生徒") {
          return {
            columns: [
              { key: "id", label: "ID", editable: false, width: "80px" },
              {
                key: "fullName",
                label: "氏名",
                editable: false,
                width: "150px",
              },
              {
                key: "grade",
                label: "学年",
                editable: true,
                width: "100px",
                type: "select",
                suffix: "年",
              },
              {
                key: "className",
                label: "クラス",
                editable: true,
                width: "100px",
                type: "select",
                suffix: "組",
              },
              {
                key: "status",
                label: "状態",
                editable: true,
                width: "120px",
                type: "select",
              },
            ],
          };
        } else if (role === "養護教諭") {
          return {
            columns: [
              { key: "id", label: "ID", editable: false, width: "100px" },
              {
                key: "fullName",
                label: "氏名",
                editable: false,
                width: "200px",
              },
              { key: "role", label: "役割", editable: false, width: "120px" },
              {
                key: "status",
                label: "状態",
                editable: true,
                width: "150px",
                type: "select",
              },
            ],
          };
        } else if (role === "管理者") {
          return {
            columns: [
              { key: "id", label: "ID", editable: false, width: "80px" },
              {
                key: "fullName",
                label: "氏名",
                editable: false,
                width: "150px",
              },
              { key: "role", label: "役割", editable: false, width: "100px" },
              {
                key: "grade",
                label: "学年",
                editable: true,
                width: "100px",
                type: "select",
                suffix: "年",
              },
              {
                key: "className",
                label: "クラス",
                editable: true,
                width: "100px",
                type: "select",
                suffix: "組",
              },
              {
                key: "status",
                label: "状態",
                editable: true,
                width: "120px",
                type: "select",
              },
            ],
          };
        }
      }

      // 複数役割混在の場合は全項目編集可能
      return {
        columns: [
          { key: "id", label: "ID", editable: false, width: "60px" },
          { key: "fullName", label: "氏名", editable: false, width: "120px" },
          { key: "role", label: "役割", editable: false, width: "80px" },
          {
            key: "teacher_role",
            label: "教員区分",
            editable: true,
            width: "110px",
            type: "select",
            options: "teacherRoles",
          },
          {
            key: "subject",
            label: "担当科目",
            editable: true,
            width: "120px",
            type: "select",
            options: "subjects",
          },
          {
            key: "grade",
            label: "学年",
            editable: true,
            width: "80px",
            type: "select",
            suffix: "年",
          },
          {
            key: "className",
            label: "クラス",
            editable: true,
            width: "80px",
            type: "select",
            suffix: "組",
          },
          {
            key: "enrollmentYear",
            label: "登録年",
            editable: true,
            width: "90px",
            suffix: "年",
          },
          {
            key: "status",
            label: "状態",
            editable: true,
            width: "100px",
            type: "select",
          },
        ],
      };
    },
  },
  methods: {
    backToSearch() {
      this.$emit("back-to-search");
    },

    backToResults() {
      this.$emit("back-to-results");
    },

    getCellValue(item, column) {
      if (column.key === "fullName") {
        const last = item.last_name || "";
        const first = item.first_name || "";
        return last + " " + first;
      }

      let value = item[column.key];

      // teacher_roleとsubjectの日本語変換
      if (column.key === "teacher_role" && value) {
        const role = this.teacherRoles.find((r) => r.code === value);
        return role ? role.name : value;
      }
      if (column.key === "subject" && value) {
        const subject = this.subjects.find((s) => s.code === value);
        return subject ? subject.name : value;
      }

      if (
        value === null ||
        value === undefined ||
        value === "" ||
        value === 0
      ) {
        return "-";
      }

      return value + (column.suffix || "");
    },

    async saveChanges(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }

      this.isSaving = true;
      this.saveMessage = "";
      this.saveSuccess = null;

      const roleMap = {
        生徒: "student",
        教師: "teacher",
        管理者: "admin",
        養護教諭: "school_nurse",
      };
      const statusMapToBackend = {
        在校: "enrolled",
        卒業: "graduated",
        転校: "transferred",
        休学: "on_leave",
        その他: "other",
      };

      try {
        const payload = this.accounts.map((item) => ({
          id: item.id,
          role: roleMap[item.role] || item.role,
          last_name: item.last_name,
          first_name: item.first_name,
          grade: parseInt(item.grade) || 0,
          className: item.className || "0",
          status: statusMapToBackend[item.status] || item.status,
          teacher_role: item.teacher_role || null,
          subject: item.subject || null,
        }));

        console.log("📤 Sending update payload:", payload);

        const response = await axios.post(
          "http://127.0.0.1:8000/account-management/update",
          payload
        );

        console.log("📗 Update response:", response.data);

        this.saveSuccess = response.data.success;
        this.saveMessage =
          response.data.message ||
          (response.data.success
            ? "変更を保存しました。"
            : "保存に失敗しました。");

        if (response.data.success) {
          this.updatedAccounts = this.accounts.map((acc) => ({ ...acc }));
          this.$nextTick(() => {
            this.showResult = true;
          });
        } else {
          this.showResult = true;
        }
      } catch (error) {
        console.error("🔴 Update error:", error);
        this.saveSuccess = false;

        if (error.response) {
          this.saveMessage =
            error.response.data.detail || "保存に失敗しました。";
        } else {
          this.saveMessage = "通信エラーが発生しました。";
        }

        this.showResult = true;
      } finally {
        this.isSaving = false;
      }
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

    getSelectOptions(column) {
      if (column.key === "grade") {
        return this.gradeOptions;
      } else if (column.key === "className") {
        return this.classOptions;
      } else if (column.key === "status") {
        return this.statusOptions;
      } else if (column.options === "teacherRoles") {
        return this.teacherRoles;
      } else if (column.options === "subjects") {
        return this.subjects;
      }
      return [];
    },

    formatSelectOption(column, option) {
      if (column.options === "teacherRoles" || column.options === "subjects") {
        return option.name;
      } else if (column.key === "grade") {
        return option === 0 ? "-" : `${option}年`;
      } else if (column.key === "className") {
        return option === "0" ? "-" : `${option}組`;
      }
      return option;
    },

    getSelectValue(column, option) {
      if (column.options === "teacherRoles" || column.options === "subjects") {
        return option.code;
      }
      return option;
    },
  },

  mounted() {
    this.accounts = this.accounts.map((acc) => {
      const role = this.teacherRoles.find((r) => r.name === acc.teacher_role);
      if (role) acc.teacher_role = role.code;

      const subject = this.subjects.find((s) => s.name === acc.subject);
      if (subject) acc.subject = subject.code;

      return acc;
    });
  },

  template: `
    <div class="d-flex justify-content-center mt-4 px-2">
      <div class="w-100" style="max-width: 1200px;">
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
            <button type="button" class="btn-close" @click="closeResult"></button>
          </div>
        </div>

        <h6 class="mb-3">更新されたアカウント情報</h6>
        <div class="card">
          <div class="table-responsive">
            <table class="table table-bordered mb-0">
            <thead class="table-light">
              <tr>
                <th v-for="col in editableColumns.columns" :key="col.key" :style="{ width: col.width }">
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
          <button type="button" class="btn btn-secondary" @click.prevent.stop="resetAndBackToResults">
            <i class="fas fa-arrow-left me-2"></i>検索結果に戻る
          </button>
          <button type="button" class="btn btn-primary" @click.prevent.stop="backToSearch">
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
            <button type="button" class="btn btn-secondary" @click.prevent.stop="backToResults">
              <i class="fas fa-arrow-left me-2"></i>検索結果に戻る
            </button>
            <button type="button" class="btn btn-outline-secondary" @click.prevent.stop="backToSearch">
              <i class="fas fa-search me-2"></i>検索画面に戻る
            </button>
          </div>
          <button type="button" class="btn btn-primary" :disabled="isSaving" @click.prevent.stop="saveChanges">
            <span v-if="isSaving" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-save me-2"></i>保存
          </button>
        </div>

        <!-- エラー表示 -->
        <div v-if="showResult && !saveSuccess" class="alert alert-danger mb-3">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <i class="fas fa-exclamation-circle me-2"></i>{{ saveMessage }}
            </div>
            <button type="button" class="btn-close" @click="closeResult"></button>
          </div>
        </div>

        <div class="card">
          <div class="table-responsive">
            <table class="table table-bordered table-hover mb-0">
            <thead class="table-light">
              <tr>
                <th v-for="col in editableColumns.columns" :key="col.key" :style="{ width: col.width }">
                  {{ col.label }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in accounts" :key="index">
                <td v-for="col in editableColumns.columns" :key="col.key">
                  <!-- 編集可能フィールド -->
                  <template v-if="col.editable">
                    <select v-if="col.type === 'select'" 
                            v-model="item[col.key]" 
                            class="form-select form-select-sm">
                      <option value="">-</option>
                      <option v-for="opt in getSelectOptions(col)" 
                              :key="getSelectValue(col, opt)" 
                              :value="getSelectValue(col, opt)">
                        {{ formatSelectOption(col, opt) }}
                      </option>
                    </select>
                    <input v-else 
                           v-model="item[col.key]" 
                           class="form-control form-control-sm">
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
  `,
};
