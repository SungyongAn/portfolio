<template>
  <div class="container mt-4">
    <!-- ページタイトル -->
    <h2 class="mb-4">測定結果の入力</h2>

    <!-- 成功メッセージ -->
    <div v-if="successMessage" class="alert alert-success">
      {{ successMessage }}
    </div>

    <!-- ③入力フォーム -->
    <form @submit.prevent="handleSubmit">
      <div class="row g-3 mb-3">
        <!-- 部員選択 -->
        <div class="col-md-6">
          <label class="form-label">
            部員選択 <span class="text-danger">*</span>
          </label>

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
          <label class="form-label">
            計測日 <span class="text-danger">*</span>
          </label>

          <input
            type="date"
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
            <div class="card-header">
              {{ category }}
            </div>

            <div class="card-body">
              <div class="row g-3">
                <div v-for="field in fields" :key="field.key" class="col-md-6">
                  <label class="form-label">
                    {{ field.label }} ({{ field.unit }})
                    <span class="text-danger">*</span>
                  </label>

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
          <span v-if="loading"> 送信中... </span>

          <span v-else> 承認依頼を送信 </span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from "vue";
import { getUsers } from "@/services/userService.js";
import {
  createMeasurement,
  submitMeasurement,
} from "@/services/measurementService.js";
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";

const members = ref([]);

onMounted(async () => {
  const res = await getUsers("member");
  members.value = res.data.users;
});

const groupedFields = computed(() => {
  const groups = {};

  MEASUREMENT_FIELDS.forEach((f) => {
    if (!groups[f.category]) {
      groups[f.category] = [];
    }

    groups[f.category].push(f);
  });

  return groups;
});

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

const loading = ref(false);
const successMessage = ref("");

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

const handleSubmit = async () => {
  if (!validate()) return;

  loading.value = true;

  try {
    // 1. 測定記録を登録
    const measurementData = Object.fromEntries(
      MEASUREMENT_FIELDS.map((f) => [f.key, form[f.key]]),
    );

    const res = await createMeasurement({
      user_id: form.userId,
      measurement_date: form.measurementDate,
      ...measurementData,
    });

    // 2. 承認依頼を送信
    await submitMeasurement(res.data.measurement_id);

    successMessage.value = "測定結果を登録し、承認依頼を送信しました";
  } catch (error) {
    console.error(error);
    successMessage.value = "";
    alert("エラーが発生しました");
  } finally {
    loading.value = false;
  }
};
</script>
