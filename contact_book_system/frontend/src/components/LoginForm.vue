<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow">
          <div class="card-header bg-primary text-white">
            <h4 class="mb-0">連絡帳システム ログイン</h4>
          </div>
          <div class="card-body">
            <div v-if="errorMessage" class="alert alert-danger">
              {{ errorMessage }}
            </div>

            <form @submit.prevent="handleLogin">
              <!-- ID入力（ローカルパート） -->
              <div class="mb-3">
                <label for="id" class="form-label">ID</label>
                <div class="input-group">
                  <input
                    type="text"
                    class="form-control"
                    id="id"
                    v-model="loginData.id"
                    autocomplete="username"
                    required
                    :disabled="isLoading"
                  />
                </div>
              </div>

              <!-- パスワード -->
              <div class="mb-3">
                <label for="password" class="form-label">パスワード</label>
                <input
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control"
                  id="password"
                  v-model="loginData.password"
                  autocomplete="current-password"
                  required
                  :disabled="isLoading"
                />

                <div class="form-check mt-2">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    id="showPassword"
                    v-model="showPassword"
                  />
                  <label for="showPassword" class="form-check-label"
                    >パスワードを表示</label
                  >
                </div>
              </div>

              <button
                type="submit"
                class="btn btn-primary w-100"
                :disabled="isLoading"
              >
                <span
                  v-if="isLoading"
                  class="spinner-border spinner-border-sm me-2"
                ></span>
                ログイン
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginForm",
  emits: ["login", "updateTitle"],
  data() {
    return {
      loginData: {
        id: "",
        password: "",
      },
      errorMessage: "",
      isLoading: false,
      showPassword: false,
    };
  },
  methods: {
    async handleLogin() {
      this.errorMessage = "";
      this.isLoading = true;

      const payload = {
        email: this.loginData.id + "@school.com",
        password: this.loginData.password,
      };

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/auth/login",
          payload
        );

        if (response.data.success) {
          const token = response.data.data.access_token;

          if (token) {
            sessionStorage.setItem("access_token", token);
            axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
          } else {
            this.errorMessage = "トークンが取得できませんでした";
            return;
          }

          const userData = {
            id: response.data.data.id,
            role: response.data.data.role,
            grade: response.data.data.grade,
            className: response.data.data.class_name,
            lastName: response.data.data.last_name,
            firstName: response.data.data.first_name,
            isTeacher: response.data.data.role === "teacher",
            teacherRole: response.data.data.teacher_role?.code || null,
            isGradeLeader:
              response.data.data.teacher_role?.code === "grade_leader",
            isHomeroomTeacher:
              response.data.data.teacher_role?.code === "homeroom",
            isAssistantTeacher:
              response.data.data.teacher_role?.code === "assistant_homeroom",
            isSubjectTeacher:
              response.data.data.teacher_role?.code === "subject_teacher",
            isAdmin: response.data.data.role === "admin",
            status: response.data.data.status,
            enrollmentYear: response.data.data.enrollment_year || 0,
            graduationYear: response.data.data.graduation_year || 0,
          };

          this.$emit("login", userData);

          this.loginData = { id: "", password: "" };
        } else {
          this.errorMessage = response.data.message || "ログインに失敗しました";
        }
      } catch (error) {
        console.error("Login error:", error);
        this.errorMessage =
          error.response?.data?.detail ||
          "ログイン処理中にエラーが発生しました";
      } finally {
        this.isLoading = false;
      }
    },
  },
  mounted() {
    // ログイン画面ではヘッダーを非表示にする
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },
  beforeUnmount() {
    // コンポーネントが破棄される時も念のためリセット
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },
};
</script>
