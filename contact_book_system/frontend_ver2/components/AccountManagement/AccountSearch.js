const AccountSearch = {
  props: ["currentUser"],
  emits: ["show-results", "back-to-menu", "updateTitle"],
  data() {
    return {
      form: {
        studentStaffNumber: "",
        role: "",
        fullName: "",
        grade: null,
        class_name: "",
        teacher_role: "",
        subject: "",
        enrollment_year: "",
        status: "",
      },
      isLoading: false,
      // ✅ AccountFormと同じマスターデータ
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
    isFormValid() {
      return Object.values(this.form).some(
        (value) => value && value.toString().trim() !== ""
      );
    },
    isTeacher() {
      return this.form.role === "教師";
    },
  },
  mounted() {
    // ヘッダーにタイトルと戻るボタンを設定
    this.$emit("updateTitle", {
      title: "アカウント検索",
      icon: "fas fa-folder-open",
      showBackButton: true,
    });
  },
  beforeUnmount() {
    // コンポーネント離脱時にタイトルをクリア
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },
  methods: {
    async searchAccounts(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }

      if (!this.isFormValid) {
        alert("いずれかの項目を入力してください");
        return;
      }

      this.isLoading = true;

      const roleMap = {
        生徒: "student",
        教師: "teacher",
        養護教諭: "school_nurse",
      };
      const roleMapReverse = {
        student: "生徒",
        teacher: "教師",
        school_nurse: "養護教諭",
      };

      // ✅ ステータスの日本語→英語変換マップ
      const statusMapToBackend = {
        在校: "enrolled",
        卒業: "graduated",
        転校: "transferred",
        休学: "on_leave",
        その他: "other",
      };

      // ✅ ステータスの英語→日本語変換マップ
      const statusMapToFrontend = {
        enrolled: "在校",
        graduated: "卒業",
        transferred: "転校",
        on_leave: "休学",
        suspended: "休学",
        other: "その他",
      };

      // ✅ payloadの構築（codeとenumで送信）
      const payload = {};
      for (const key in this.form) {
        if (this.form[key]) {
          if (key === "role") {
            payload[key] = roleMap[this.form[key]];
          } else if (key === "status") {
            // ✅ 日本語のステータスを英語に変換
            payload[key] = statusMapToBackend[this.form[key]] || this.form[key];
          } else if (key === "grade") {
            payload[key] = parseInt(this.form[key]);
          } else if (key === "enrollment_year") {
            payload[key] = parseInt(this.form[key]);
          } else {
            // teacher_role, subject, class_name はそのまま送信
            payload[key] = this.form[key];
          }
        }
      }

      console.log("Sending search payload:", payload); // デバッグ用

      try {
        const response = await axios.post(
          "/account-management/search",
          payload
        );

        const data = response.data;
        let results = [];
        let resultType = "success";
        let resultMessage = "";

        if (data.success) {
          results = data.data || [];

          // ✅ codeとenumを日本語に変換して表示
          results = results.map((item) => {
            const converted = { ...item };

            // roleを日本語に変換
            converted.role = roleMapReverse[item.role] || item.role;

            // ✅ statusを日本語に変換
            converted.status = statusMapToFrontend[item.status] || "その他";

            // teacher_roleを日本語に変換
            if (item.teacher_role) {
              const role = this.teacherRoles.find(
                (r) => r.code === item.teacher_role
              );
              converted.teacher_role = role ? role.name : item.teacher_role;
            }

            // subjectを日本語に変換
            if (item.subject) {
              const subject = this.subjects.find(
                (s) => s.code === item.subject
              );
              converted.subject = subject ? subject.name : item.subject;
            }

            return converted;
          });

          resultMessage =
            results.length > 0
              ? `${results.length}件のアカウントが見つかりました`
              : "該当するアカウントはありません";
        } else {
          resultType = "error";
          resultMessage = data.message || "検索に失敗しました";
        }

        this.$emit("show-results", { results, resultType, resultMessage });
      } catch (error) {
        console.error("🔴 検索エラー:", error);
        let errorMessage = "通信エラーが発生しました";
        if (error.response) {
          errorMessage =
            error.response.data.detail ||
            error.response.data.message ||
            errorMessage;
        }
        this.$emit("show-results", {
          results: [],
          resultType: "error",
          resultMessage: errorMessage,
        });
      } finally {
        this.isLoading = false;
      }
    },

    resetForm() {
      this.form = {
        studentStaffNumber: "",
        role: "",
        fullName: "",
        grade: null,
        class_name: "",
        teacher_role: "",
        subject: "",
        enrollment_year: "",
        status: "",
      };
    },
  },
  template: `
    <div class="d-flex justify-content-center align-items-center" style="min-height: 85vh;">
      <div class="card p-4 shadow-sm" style="max-width: 700px; width: 100%;">

        <form @submit.prevent.stop="searchAccounts">

          <!-- 1行目: 生徒・職員番号 + 役割 -->
          <div class="row g-3 mb-2">
            <div class="col-md-6">
              <label class="form-label">生徒・職員番号</label>
              <input type="text" v-model="form.studentStaffNumber" class="form-control"
                     placeholder="例：S12345" :disabled="isLoading">
            </div>
            <div class="col-md-6">
              <label class="form-label">役割</label>
              <select v-model="form.role" class="form-select" :disabled="isLoading">
                <option value="">--選択--</option>
                <option value="生徒">生徒</option>
                <option value="教師">教師</option>
                <option value="養護教諭">養護教諭</option>
              </select>
            </div>
          </div>

          <!-- 2行目: 氏名 + 教員区分 -->
          <div class="row g-3 mb-2">
            <div class="col-md-6">
              <label class="form-label">氏名</label>
              <input type="text" v-model="form.fullName" class="form-control"
                     placeholder="例：山田 太郎" :disabled="isLoading">
            </div>
            <div class="col-md-6">
              <label class="form-label">教員区分</label>
              <select v-model="form.teacher_role" class="form-select" :disabled="isLoading">
                <option value="">--選択--</option>
                <option v-for="role in teacherRoles" :key="role.code" :value="role.code">
                  {{ role.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- 3行目: 登録年 + 担当科目 -->
          <div class="row g-3 mb-2">
            <div class="col-md-6">
              <label class="form-label">登録年</label>
              <input type="text" v-model="form.enrollment_year" class="form-control"
                     placeholder="例：2023" :disabled="isLoading">
            </div>
            <div class="col-md-6">
              <label class="form-label">担当科目</label>
              <select v-model="form.subject" class="form-select" :disabled="isLoading">
                <option value="">--選択--</option>
                <option v-for="subject in subjects" :key="subject.code" :value="subject.code">
                  {{ subject.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- 4行目: 学年 + クラス -->
          <div class="row g-3 mb-2">
            <div class="col-md-6">
              <label class="form-label">学年</label>
              <select v-model.number="form.grade" class="form-select" :disabled="isLoading">
                <option :value="null">--選択--</option>
                <option :value="1">1年</option>
                <option :value="2">2年</option>
                <option :value="3">3年</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">クラス</label>
              <select v-model="form.class_name" class="form-select" :disabled="isLoading">
                <option value="">--選択--</option>
                <option value="A">A組</option>
                <option value="B">B組</option>
                <option value="C">C組</option>
              </select>
            </div>
          </div>

          <!-- 5行目: 状態 -->
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label">状態</label>
              <select v-model="form.status" class="form-select" :disabled="isLoading">
                <option value="">--選択--</option>
                <option value="在校">在校</option>
                <option value="卒業">卒業</option>
                <option value="転校">転校</option>
                <option value="休学">休学</option>
                <option value="その他">その他</option>
              </select>
            </div>
          </div>

          <!-- ボタン行 -->
          <div class="text-center">
            <button type="submit" class="btn btn-primary me-2 px-4"
                    :disabled="isLoading || !isFormValid">
              <span v-if="isLoading">
                <span class="spinner-border spinner-border-sm me-2"></span>検索中...
              </span>
              <span v-else><i class="fas fa-search me-2"></i>検索</span>
            </button>

            <button type="button" @click="resetForm" class="btn btn-secondary me-2 px-4" :disabled="isLoading">
              <i class="fas fa-redo me-2"></i>リセット
            </button>

          </div>
        </form>
      </div>
    </div>
  `,
};
