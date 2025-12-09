const AccountForm = {
  emits: ["back-to-menu", "updateTitle"],
  data() {
    const currentYear = new Date().getFullYear();
    return {
      accountForm: {
        studentNumber: "",
        role: "生徒",
        last_name: "",
        first_name: "",
        grade: null,
        class_name: "",
        teacher_role: "",
        subject: "",
        password: "",
        confirmPassword: "",
        enrollment_year: currentYear,
      },
      showPassword: false,
      showConfirmPassword: false,
      registeredAccount: null,
      errorMessage: "",
      isLoading: false,
      // 教員区分
      teacherRoles: [
        { code: "grade_leader", name: "学年主任" },
        { code: "homeroom_teacher", name: "担任" },
        { code: "assistant_teacher", name: "副担任" },
        { code: "subject_teacher", name: "教科担当" },
      ],
      // 科目
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
    graduationYear() {
      if (this.accountForm.role !== "生徒") return 0;
      const year = parseInt(this.accountForm.enrollment_year);
      const grade = parseInt(this.accountForm.grade);
      if (!year || !grade) return null;

      const month = new Date().getMonth() + 1;

      let graduation = year + (4 - grade);

      return graduation;
    },
    isTeacher() {
      return this.accountForm.role === "教師";
    },
    isSchoolNurse() {
      return this.accountForm.role === "養護教諭";
    },
    displayRegisteredAccount() {
      if (!this.registeredAccount) return null;
      const result = { ...this.registeredAccount };

      const roleMap = {
        student: "生徒",
        teacher: "教師",
        school_nurse: "養護教諭",
      };
      if (result.role) result.role = roleMap[result.role] || result.role;

      if (result.teacher_role) {
        const role = this.teacherRoles.find(
          (r) => r.code === result.teacher_role
        );
        result.teacher_role = role ? role.name : result.teacher_role;
      }

      if (result.subject) {
        const subject = this.subjects.find((s) => s.code === result.subject);
        result.subject = subject ? subject.name : result.subject;
      }

      return result;
    },
    resultFields() {
      return [
        { label: "ID", key: "email" },
        { label: "姓", key: "last_name" },
        { label: "名", key: "first_name" },
        { label: "学年", key: "grade", suffix: "年" },
        { label: "クラス", key: "class_name", suffix: "組" },
        { label: "役割", key: "role" },
        { label: "教員区分", key: "teacher_role" },
        { label: "担当科目", key: "subject" },
        { label: "登録年", key: "enrollment_year", suffix: "年" },
        { label: "卒業予定年", key: "graduation_year", suffix: "年" },
      ];
    },
  },
  mounted() {
    this.$emit("updateTitle", {
      title: "新規アカウントの作成",
      icon: "fas fa-folder-open",
      showBackButton: true,
    });
  },
  beforeUnmount() {
    this.$emit("updateTitle", { title: "", icon: "", showBackButton: false });
  },
  methods: {
    async handleCreateAccount(event) {
      if (event) event.preventDefault();

      if (!this.accountForm.studentNumber) {
        this.errorMessage = "生徒・職員IDを入力してください";
        return;
      }

      if (
        !this.accountForm.last_name ||
        !this.accountForm.first_name ||
        !this.accountForm.password ||
        !this.accountForm.enrollment_year ||
        (this.isTeacher && !this.accountForm.teacher_role)
      ) {
        this.errorMessage = "すべての必須項目を入力してください";
        return;
      }
      if (this.accountForm.password !== this.accountForm.confirmPassword) {
        this.errorMessage = "パスワードが一致しません";
        return;
      }

      this.isLoading = true;
      this.errorMessage = "";

      try {
        const roleMap = {
          生徒: "student",
          教師: "teacher",
          養護教諭: "school_nurse",
        };

        let gradeValue = 0,
          classValue = "0";
        if (this.accountForm.role === "生徒") {
          gradeValue = parseInt(this.accountForm.grade);
          classValue = this.accountForm.class_name;
        } else if (this.isTeacher) {
          const selectedRole = this.teacherRoles.find(
            (r) => r.code === this.accountForm.teacher_role
          );
          if (selectedRole) {
            switch (selectedRole.code) {
              case "grade_leader":
                gradeValue = parseInt(this.accountForm.grade);
                classValue = "0";
                break;
              case "homeroom_teacher":
              case "assistant_teacher":
                gradeValue = parseInt(this.accountForm.grade);
                classValue = this.accountForm.class_name;
                break;
              default:
                gradeValue = 0;
                classValue = "0";
            }
          }
        }

        const payload = {
          email: this.accountForm.studentNumber + "@school.com", // ← これを追加
          role: roleMap[this.accountForm.role] || "student",
          last_name: this.accountForm.last_name,
          first_name: this.accountForm.first_name,
          grade: gradeValue,
          class_name: classValue,
          password: this.accountForm.password,
          enrollment_year: parseInt(this.accountForm.enrollment_year),
          graduation_year: this.graduationYear || 2099,
          teacher_role:
            this.isTeacher && this.accountForm.teacher_role
              ? this.accountForm.teacher_role
              : null,
          subject:
            this.isTeacher && this.accountForm.subject
              ? this.accountForm.subject
              : null,
        };

        console.log("Sending payload:", payload);

        const response = await axios.post(
          "http://127.0.0.1:8000/account-management/register",
          payload
        );

        if (response.data.success) {
          this.registeredAccount = response.data.data;
        } else {
          this.errorMessage =
            response.data.message || "アカウント作成に失敗しました";
        }
      } catch (err) {
        console.error(err);
        this.errorMessage =
          err.response?.data?.detail ||
          err.response?.data?.message ||
          "アカウント作成に失敗しました。";
      } finally {
        this.isLoading = false;
      }
    },
    resetToNewRegistration() {
      const currentYear = new Date().getFullYear();
      this.registeredAccount = null;
      this.accountForm = {
        studentNumber: "",
        role: "生徒",
        fullName: "",
        grade: null,
        class_name: "",
        teacher_role: "",
        subject: "",
        password: "",
        confirmPassword: "",
        enrollment_year: currentYear,
      };
      this.errorMessage = "";
    },
    backToMenu() {
      this.$emit("back-to-menu");
    },
  },
  template: `
<div class="d-flex justify-content-center mt-5 px-2">
  <div class="card p-4 w-100" style="max-width:700px;">

    <!-- 登録結果表示 -->
    <template v-if="registeredAccount">
      <div class="alert alert-success mb-3">
        <i class="fas fa-check-circle me-2"></i>アカウントが正常に作成されました。
      </div>
      <h6 class="mb-3">登録済みアカウント情報</h6>
      <table class="table table-bordered bg-white">
        <tbody>
          <tr v-for="field in resultFields" :key="field.key">
            <th class="bg-light" style="width:150px;">{{field.label}}</th>
            <td>{{ displayRegisteredAccount[field.key] || '-' }}{{ field.suffix||'' }}</td>
          </tr>
        </tbody>
      </table>
      <div class="d-flex justify-content-center gap-2 mt-4">
        <button class="btn btn-primary btn-lg" @click="resetToNewRegistration">
          <i class="fas fa-plus-circle me-2"></i>新しいアカウントを作成
        </button>
      </div>
    </template>

    <!-- 新規登録フォーム -->
    <template v-else>
      <div v-if="errorMessage" class="alert alert-danger">{{errorMessage}}</div>
      <form @submit.prevent="handleCreateAccount">

        <!-- 1行目: 生徒・職員番号 + 登録年 -->
        <div class="row mb-3">
          <div class="col-md-6">
            <label class="form-label">生徒・職員ID <span class="text-danger">*</span></label>
            <div class="input-group">
              <input
                type="text" 
                class="form-control" 
                v-model="accountForm.studentNumber" 
                :disabled="isLoading" 
                placeholder="例: tanaka.taro"
                required
              >
              <span class="input-group-text">@school.com</span>
            </div>
            <small class="text-muted">ローカルパートがログイン時のIDとして使用されます</small>
          </div>
          <div class="col-md-6">
            <label class="form-label">登録年</label>
            <input type="text" class="form-control" v-model="accountForm.enrollment_year" disabled>
          </div>
        </div>

        <!-- 2行目: 氏名 + 役割 -->
        <div class="row mb-3">
          <div class="col-md-3">
            <label class="form-label">姓 <span class="text-danger">*</span></label>
            <input
              type="text"
              class="form-control"
              v-model="accountForm.last_name"
              :disabled="isLoading"
              required
            >
          </div>

          <div class="col-md-3">
            <label class="form-label">名 <span class="text-danger">*</span></label>
            <input
              type="text"
              class="form-control"
              v-model="accountForm.first_name"
              :disabled="isLoading"
              required
            >
          </div>
          <div class="col-md-6">
            <label class="form-label">役割 <span class="text-danger">*</span></label>
            <select class="form-select" v-model="accountForm.role" :disabled="isLoading">
              <option value="生徒">生徒</option>
              <option value="教師">教師</option>
              <option value="養護教諭">養護教諭</option>
            </select>
          </div>
        </div>

        <!-- 3行目: 教員区分 + 担当科目（教師のみ表示） -->
        <div class="row mb-3" v-if="isTeacher">
          <div class="col-md-6">
            <label class="form-label">教員区分 <span class="text-danger">*</span></label>
            <select class="form-select" v-model="accountForm.teacher_role" :disabled="isLoading">
              <option value="">選択してください</option>
              <option v-for="role in teacherRoles" :key="role.code" :value="role.code">
                {{ role.name }}
              </option>
            </select>
          </div>
          <div class="col-md-6">
            <label class="form-label">担当科目</label>
            <select class="form-select" v-model="accountForm.subject" :disabled="isLoading">
              <option value="">選択してください</option>
              <option v-for="subject in subjects" :key="subject.code" :value="subject.code">
                {{ subject.name }}
              </option>
            </select>
          </div>
        </div>

        <!-- 学年 + クラス（生徒・担任・副担任のみ表示） -->
        <div class="row mb-3" v-if="(accountForm.role !== '養護教諭' && !isTeacher) || 
                                        (isTeacher && accountForm.teacher_role && 
                                         teacherRoles.find(r => ['grade_leader','homeroom_teacher','assistant_teacher'].includes(r.code)))">
          <div class="col-md-6">
            <label class="form-label">学年 <span class="text-danger">*</span></label>
            <select class="form-select" v-model.number="accountForm.grade" :disabled="isLoading">
              <option :value="null">選択してください</option>
              <option :value="1">1年</option>
              <option :value="2">2年</option>
              <option :value="3">3年</option>
            </select>
          </div>
          <div class="col-md-6" v-if="(accountForm.role !== '養護教諭' && !isTeacher) || 
                                       (isTeacher && ['homeroom_teacher','assistant_teacher'].includes(accountForm.teacher_role))">
            <label class="form-label">クラス <span class="text-danger">*</span></label>
            <select class="form-select" v-model="accountForm.class_name" :disabled="isLoading">
              <option value="">選択してください</option>
              <option value="A">A組</option>
              <option value="B">B組</option>
              <option value="C">C組</option>
            </select>
          </div>
        </div>

        <!-- パスワード入力 -->
        <div class="mb-3">
          <label class="form-label">パスワード <span class="text-danger">*</span></label>
          <div class="input-group">
            <input :type="showPassword ? 'text' : 'password'" class="form-control" v-model="accountForm.password" :disabled="isLoading">
            <button class="btn btn-outline-secondary" type="button" @click="showPassword = !showPassword">
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label">パスワード(確認) <span class="text-danger">*</span></label>
          <div class="input-group">
            <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control" v-model="accountForm.confirmPassword" :disabled="isLoading">
            <button class="btn btn-outline-secondary" type="button" @click="showConfirmPassword = !showConfirmPassword">
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
          <small v-if="accountForm.confirmPassword && accountForm.password !== accountForm.confirmPassword" class="text-danger">
            パスワードが一致しません
          </small>
        </div>

        <!-- ボタン -->
        <div class="d-flex justify-content-end gap-2 flex-wrap">
          <button class="btn btn-secondary" type="button" @click="resetToNewRegistration" :disabled="isLoading">リセット</button>
          <button class="btn btn-success" type="button" @click="handleCreateAccount" :disabled="isLoading">作成</button>
        </div>

      </form>
    </template>
  </div>
</div>
`,
};
