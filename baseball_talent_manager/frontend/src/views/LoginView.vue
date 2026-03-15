<template>
  <div class="login-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <div class="text-center mb-4">
                <i class="bi bi-journal-text display-1 text-primary"></i>
                <h2 class="mt-3">野球部タレントマネジメントシステム</h2>
                <p class="text-muted">メールアドレスとパスワードでログイン</p>
              </div>

              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="email" class="form-label">メールアドレス</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-envelope"></i>
                    </span>
                    <input
                      type="email"
                      class="form-control"
                      id="email"
                      v-model="email"
                      placeholder="example@jpt.com"
                      required
                      :disabled="loading"
                    />
                  </div>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label">パスワード</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="bi bi-lock"></i>
                    </span>
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      id="password"
                      v-model="password"
                      placeholder="パスワードを入力"
                      required
                      :disabled="loading"
                    />
                    <button
                      class="btn btn-outline-secondary"
                      type="button"
                      @click="showPassword = !showPassword"
                    >
                      <i
                        :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"
                      ></i>
                    </button>
                  </div>
                </div>

                <div
                  v-if="errorMessage"
                  class="alert alert-danger"
                  role="alert"
                >
                  <i class="bi bi-exclamation-triangle"></i>
                  {{ errorMessage }}
                </div>

                <button
                  type="submit"
                  class="btn btn-primary w-100 py-2"
                  :disabled="loading"
                >
                  <span v-if="loading">
                    <span class="spinner-border spinner-border-sm me-2"></span>
                    ログイン中...
                  </span>
                  <span v-else>
                    <i class="bi bi-box-arrow-in-right me-2"></i>
                    ログイン
                  </span>
                </button>
              </form>

              <hr class="my-4" />

              <div class="text-center">
                <small class="text-muted">
                  <strong>テストアカウント</strong><br />
                  山田 花子: manager@jpt.com<br />
                  田中 太郎: member1@jpt.com<br />
                  伊藤 コーチ: coach@jpt.com<br />
                  渡辺 監督: director@jpt.com<br />
                  パスワード: test123
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const email = ref("");
const password = ref("");
const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");

const handleLogin = async () => {
  loading.value = true;
  errorMessage.value = "";

  try {
    await authStore.login(email.value, password.value);

    router.push("/");
  } catch (error) {
    console.error(error);
    errorMessage.value = "ログインに失敗しました";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card {
  border-radius: 1rem;
}

.input-group-text {
  background-color: #f8f9fa;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5568d3 0%, #66408b 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.3s;
}
</style>
