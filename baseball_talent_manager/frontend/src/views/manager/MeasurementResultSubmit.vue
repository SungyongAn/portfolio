<template>
  <div class="container mt-4">
    <h2 class="mb-4">測定結果の入力</h2>

    <!-- 成功メッセージ -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <!-- エラーメッセージ -->
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <!-- 入力フォーム -->
    <form @submit.prevent="handleSubmit">
      <div class="row g-3 mb-3">
        <!-- 部員選択 -->
        <div class="col-md-6">
          <label class="form-label"
            >部員選択 <span class="text-danger">*</span></label
          >
          <select
            v-model="form.userId"
            class="form-select"
            :class="{ 'is-invalid': errors.userId }"
          >
            <option disabled value="">部員を選択してください</option>
            <option
              v-for="member in members"
              :key="member.user_id"
              :value="member.user_id"
            >
              {{ member.grade }}年 {{ member.name }}
            </option>
          </select>
          <div v-if="errors.userId" class="invalid-feedback">
            部員を選択してください
          </div>
        </div>

        <!-- 計測日 -->
        <div class="col-md-6">
          <label class="form-label"
            >計測日 <span class="text-danger">*</span></label
          >
          <input
            type="month"
            v-model="form.measurementDate"
            class="form-control"
            :class="{ 'is-invalid': errors.measurementDate }"
          />
          <div v-if="errors.measurementDate" class="invalid-feedback">
            計測日を入力してください
          </div>
        </div>
      </div>

      <!-- 測定項目 -->
      <div class="row g-3">
        <div
          v-for="(fields, category) in groupedFields"
          :key="category"
          class="col-md-6"
        >
          <div class="card h-100">
            <div class="card-header">{{ category }}</div>
            <div class="card-body">
              <div class="row g-3">
                <div v-for="field in fields" :key="field.key" class="col-md-6">
                  <label class="form-label"
                    >{{ field.label }} ({{ field.unit }})
                    <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    :step="field.step"
                    v-model="form[field.key]"
                    class="form-control"
                    :class="{ 'is-invalid': errors[field.key] }"
                    :placeholder="field.placeholder"
                  />
                  <div v-if="errors[field.key]" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ボタン -->
      <div class="d-flex justify-content-end gap-2 mt-4">
        <router-link to="/manager/dashboard" class="btn btn-outline-secondary">
          キャンセル
        </router-link>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          <span v-if="loading">送信中...</span>
          <span v-else>確認</span>
        </button>
      </div>
    </form>

    <!-- 確認モーダル -->
    <div
      v-if="showModal"
      class="modal d-block"
      tabindex="-1"
      style="background-color: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">入力内容の確認</h5>
          </div>
          <div class="modal-body">
            <table class="table">
              <tbody>
                <tr>
                  <th>部員</th>
                  <td>
                    {{ selectedMember.grade }}年 {{ selectedMember.name }}
                  </td>
                </tr>
                <tr>
                  <th>計測日</th>
                  <td>{{ form.measurementDate }}</td>
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
              @click="handleConfirm"
            >
              承認依頼を送信
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from "vue";
import { getUsers } from "@/services/userService.js";
import {
  createMeasurement,
  submitMeasurement,
} from "@/services/measurementService.js";
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields.js";

const members = ref([]);
const showModal = ref(false);
const loading = ref(false);
const successMessage = ref("");
const errorMessage = ref("");
const selectedMember = computed(() =>
  members.value.find((m) => m.user_id === form.userId),
);

const form = reactive({
  userId: "",
  measurementDate: "",
  ...Object.fromEntries(MEASUREMENT_FIELDS.map((f) => [f.key, null])),
});

const errors = reactive({
  userId: false,
  measurementDate: false,
  ...Object.fromEntries(MEASUREMENT_FIELDS.map((f) => [f.key, false])),
});

// 入力バリデーション
const validate = () => {
  let valid = true;
  Object.keys(form).forEach((key) => {
    if (!form[key]) {
      errors[key] = true;
      valid = false;
    } else {
      errors[key] = false;
    }
  });
  return valid;
};

// モーダル表示前に入力チェック
const handleSubmit = () => {
  if (!validate()) return;
  errorMessage.value = "";
  successMessage.value = "";
  showModal.value = true;
};

// 確認モーダルで承認依頼まで送信
const handleConfirm = async () => {
  loading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    // 1. 測定記録を登録（新規 or 上書き更新）
    const measurementData = Object.fromEntries(
      MEASUREMENT_FIELDS.map((f) => [f.key, form[f.key]]),
    );

    const res = await createMeasurement({
      user_id: form.userId,
      measurement_date: form.measurementDate + "-01",
      ...measurementData,
    });

    // 2. 承認依頼を送信（上書き更新も含む）
    await submitMeasurement(res.data.measurement_id);

    // 3. 成功メッセージ
    successMessage.value = "測定結果を登録し、承認依頼を送信しました";

    // 4. モーダル閉じてフォームリセット
    showModal.value = false;
    form.userId = "";
    form.measurementDate = "";
    MEASUREMENT_FIELDS.forEach((f) => (form[f.key] = null));
  } catch (error) {
    console.error(error);

    // エラー種別に応じた表示
    if (error.response?.status === 400) {
      errorMessage.value =
        error.response.data.detail || "同じ日の測定記録が既に存在します";
    } else if (error.response?.status === 404) {
      errorMessage.value =
        error.response.data.detail || "指定された部員が見つかりません";
    } else if (error.code === "ERR_NETWORK") {
      errorMessage.value = "サーバーに接続できません";
    } else {
      errorMessage.value = "エラーが発生しました";
    }

    showModal.value = false;
  } finally {
    loading.value = false;
  }
};

// 初回メンバー取得
onMounted(async () => {
  // 当月を初期値として設定
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  form.measurementDate = `${yyyy}-${mm}`;

  const res = await getUsers("member");
  members.value = res.data.users;
});

const groupedFields = computed(() => {
  const groups = {};
  MEASUREMENT_FIELDS.forEach((f) => {
    if (!groups[f.category]) groups[f.category] = [];
    groups[f.category].push(f);
  });
  return groups;
});
</script>
