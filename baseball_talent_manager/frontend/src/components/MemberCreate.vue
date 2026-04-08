<template>
  <div class="container mt-4">
    <h2 class="mb-4">部員作成</h2>

    <!-- 成功メッセージ -->
    <div v-if="successMessage" class="alert alert-success">
      <i class="bi bi-check-circle me-2"></i>
      {{ successMessage }}
    </div>

    <!-- 入力フォーム -->
    <form @submit.prevent="handleSubmit">
      <!-- メールアドレス -->
      <div class="mb-3">
        <label class="form-label"
          >メールアドレス <span class="text-danger">*</span></label
        >
        <input
          type="email"
          v-model="form.email"
          class="form-control"
          :class="{ 'is-invalid': errors.email }"
          placeholder="例：member@jpt.com"
        />
        <div v-if="errors.email" class="invalid-feedback">
          メールアドレスを入力してください
        </div>
      </div>

      <!-- 生徒名 -->
      <div class="mb-3">
        <label class="form-label"
          >生徒名 <span class="text-danger">*</span></label
        >
        <input
          type="text"
          v-model="form.name"
          class="form-control"
          :class="{ 'is-invalid': errors.name }"
          placeholder="例：山田 太郎"
        />
        <div v-if="errors.name" class="invalid-feedback">
          生徒名を入力してください
        </div>
      </div>

      <!-- 学年 -->
      <div class="mb-3">
        <label class="form-label"
          >学年 <span class="text-danger">*</span></label
        >
        <select
          v-model="form.grade"
          class="form-select"
          :class="{ 'is-invalid': errors.grade }"
        >
          <option disabled value="">学年を選択してください</option>
          <option value="1">1年</option>
          <option value="2">2年</option>
          <option value="3">3年</option>
        </select>
        <div v-if="errors.grade" class="invalid-feedback">
          学年を選択してください
        </div>
      </div>

      <!-- パスワード -->
      <div class="mb-3">
        <label class="form-label"
          >パスワード <span class="text-danger">*</span></label
        >
        <input
          type="password"
          v-model="form.password"
          class="form-control"
          :class="{ 'is-invalid': errors.password }"
          placeholder="パスワードを入力してください"
        />
        <div v-if="errors.password" class="invalid-feedback">
          パスワードを入力してください
        </div>
      </div>

      <!-- ボタン -->
      <div class="d-flex justify-content-end gap-2 mt-4">
        <router-link :to="`/${role}/members`" class="btn btn-outline-secondary">
          キャンセル
        </router-link>
        <button type="submit" class="btn btn-primary">確認</button>
      </div>
    </form>

    <!-- 確認モーダル -->
    <div
      v-if="showModal"
      class="modal d-block"
      tabindex="-1"
      style="background-color: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">登録内容の確認</h5>
          </div>
          <div class="modal-body">
            <table class="table">
              <tbody>
                <tr>
                  <th>メールアドレス</th>
                  <td>{{ form.email }}</td>
                </tr>
                <tr>
                  <th>生徒名</th>
                  <td>{{ form.name }}</td>
                </tr>
                <tr>
                  <th>学年</th>
                  <td>{{ form.grade }}年</td>
                </tr>
                <tr>
                  <th>パスワード</th>
                  <td>{{ "*".repeat(form.password.length) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="showModal = false"
            >
              戻る
            </button>
            <button
              type="button"
              class="btn btn-primary"
              @click="handleRegister"
            >
              登録
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { createUser } from "@/services/userService.js";

const authStore = useAuthStore();
const role = computed(() => authStore.role);

// フォームデータ
const form = reactive({
  email: "",
  name: "",
  grade: "",
  password: "",
});

// エラー状態
const errors = reactive({
  email: false,
  name: false,
  grade: false,
  password: false,
});

// 状態管理
const showModal = ref(false);
const successMessage = ref("");

// バリデーション
const validate = () => {
  let isValid = true;
  Object.keys(form).forEach((key) => {
    if (form[key] === null || form[key] === "") {
      errors[key] = true;
      isValid = false;
    } else {
      errors[key] = false;
    }
  });
  return isValid;
};

// 確認ボタン押下
const handleSubmit = () => {
  if (!validate()) return;
  showModal.value = true;
};

// 登録ボタン押下
const handleRegister = async () => {
  try {
    await createUser({
      email: form.email,
      name: form.name,
      grade: parseInt(form.grade),
      password: form.password,
      role: "member",
    });

    showModal.value = false;
    successMessage.value = `${form.name}さんのアカウントを作成しました`;

    // フォームリセット
    Object.keys(form).forEach((key) => {
      form[key] = "";
    });
  } catch (error) {
    console.error(error);
    showModal.value = false;
    alert("エラーが発生しました");
  }
};
</script>
