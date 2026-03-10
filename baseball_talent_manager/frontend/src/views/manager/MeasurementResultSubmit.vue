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
              v-for="member in MEMBERS"
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
                    {{ field.label }}
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
import { reactive, ref, computed } from "vue";
import { dummyMembers } from "@/dummyData";

const MEMBERS = dummyMembers;

const MEASUREMENT_FIELDS = [
  {
    key: "sprint_50m",
    label: "50m走 (sec)",
    step: "0.01",
    placeholder: "例：6.30",
    category: "走力",
  },

  {
    key: "baseRunning",
    label: "ベースランニング (sec)",
    step: "0.01",
    placeholder: "例：12.50",
    category: "走力",
  },

  {
    key: "throwingDistance",
    label: "遠投 (m)",
    step: "0.1",
    placeholder: "例：64",
    category: "肩力",
  },

  {
    key: "pitchSpeed",
    label: "ストレート球速 (km/h)",
    step: "0.1",
    placeholder: "例：118",
    category: "肩力",
  },

  {
    key: "battingSpeed",
    label: "打球速度 (km/h)",
    step: "0.1",
    placeholder: "例：108",
    category: "打力",
  },

  {
    key: "swingSpeed",
    label: "スイング速度 (km/h)",
    step: "0.1",
    placeholder: "例：111",
    category: "打力",
  },

  {
    key: "benchPress",
    label: "ベンチプレス (kg)",
    step: "0.1",
    placeholder: "例：65",
    category: "筋力",
  },

  {
    key: "squat",
    label: "スクワット (kg)",
    step: "0.1",
    placeholder: "例：90",
    category: "筋力",
  },
];

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

  setTimeout(() => {
    successMessage.value = "測定結果を登録し、承認依頼を送信しました";

    loading.value = false;
  }, 800);
};
</script>
