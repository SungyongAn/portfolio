<template>
  <div class="container mt-4">
    <!-- ①ページタイトル -->
    <h2 class="mb-4">測定結果の入力</h2>

    <!-- ②成功・エラーメッセージ -->
    <div v-if="successMessage" class="alert alert-success">
      <i class="bi bi-check-circle me-2"></i>
      {{ successMessage }}
    </div>

    <!-- ③入力フォーム -->
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

      <div class="row g-3">
        <!-- 走力 -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">走力</div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label"
                    >50m走 (sec) <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.01"
                    v-model="form.sprint50m"
                    class="form-control"
                    :class="{ 'is-invalid': errors.sprint50m }"
                    placeholder="例：6.30"
                  />
                  <div v-if="errors.sprint50m" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="form-label"
                    >ベースランニング (sec)
                    <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.01"
                    v-model="form.baseRunning"
                    class="form-control"
                    :class="{ 'is-invalid': errors.baseRunning }"
                    placeholder="例：12.50"
                  />
                  <div v-if="errors.baseRunning" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 肩力 -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">肩力</div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label"
                    >遠投 (m) <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.1"
                    v-model="form.throwingDistance"
                    class="form-control"
                    :class="{ 'is-invalid': errors.throwingDistance }"
                    placeholder="例：64"
                  />
                  <div v-if="errors.throwingDistance" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="form-label"
                    >ストレート球速 (km/h)
                    <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.1"
                    v-model="form.pitchSpeed"
                    class="form-control"
                    :class="{ 'is-invalid': errors.pitchSpeed }"
                    placeholder="例：118"
                  />
                  <div v-if="errors.pitchSpeed" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 打力 -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">打力</div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label"
                    >打球速度 (km/h) <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.1"
                    v-model="form.battingSpeed"
                    class="form-control"
                    :class="{ 'is-invalid': errors.battingSpeed }"
                    placeholder="例：108"
                  />
                  <div v-if="errors.battingSpeed" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="form-label"
                    >スイング速度 (km/h)
                    <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.1"
                    v-model="form.swingSpeed"
                    class="form-control"
                    :class="{ 'is-invalid': errors.swingSpeed }"
                    placeholder="例：111"
                  />
                  <div v-if="errors.swingSpeed" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 筋力 -->
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-header">筋力</div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label"
                    >ベンチプレス (kg) <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.1"
                    v-model="form.benchPress"
                    class="form-control"
                    :class="{ 'is-invalid': errors.benchPress }"
                    placeholder="例：65"
                  />
                  <div v-if="errors.benchPress" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
                <div class="col-md-6">
                  <label class="form-label"
                    >スクワット (kg) <span class="text-danger">*</span></label
                  >
                  <input
                    type="number"
                    step="0.1"
                    v-model="form.squat"
                    class="form-control"
                    :class="{ 'is-invalid': errors.squat }"
                    placeholder="例：90"
                  />
                  <div v-if="errors.squat" class="invalid-feedback">
                    入力してください
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 送信ボタン -->
      <div class="d-flex justify-content-end gap-2 mt-4">
        <router-link to="/manager/dashboard" class="btn btn-outline-secondary">
          キャンセル
        </router-link>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          <span v-if="loading">
            <span class="spinner-border spinner-border-sm me-2"></span>
            送信中...
          </span>
          <span v-else>
            <i class="bi bi-send me-2"></i>
            承認依頼を送信
          </span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import { dummyMembers } from "@/dummyData";

// 部員一覧
const members = ref([]);

// 送信データ
const form = reactive({
  userId: null,
  measurementDate: null,
  sprint50m: null,
  baseRunning: null,
  throwingDistance: null,
  pitchSpeed: null,
  battingSpeed: null,
  swingSpeed: null,
  benchPress: null,
  squat: null,
});

// エラー状態
const errors = reactive({
  userId: false,
  measurementDate: false,
  sprint50m: false,
  baseRunning: false,
  throwingDistance: false,
  pitchSpeed: false,
  battingSpeed: false,
  swingSpeed: false,
  benchPress: false,
  squat: false,
});

// 状態管理
const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

// 部員一覧取得
onMounted(() => {
  members.value = dummyMembers;
});

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

// 送信処理
const handleSubmit = async () => {
  if (!validate()) return;

  loading.value = true;
  try {
    successMessage.value = "測定結果を登録し、承認依頼を送信しました";
  } catch (e) {
    errorMessage.value = "送信に失敗しました";
  } finally {
    loading.value = false;
  }
};
</script>
