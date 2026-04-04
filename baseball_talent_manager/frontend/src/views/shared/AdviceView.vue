<template>
  <div class="container mt-4">
    <h2 class="mb-4">AIアドバイス</h2>

    <!-- 部員選択 -->
    <div class="card shadow-sm mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-md-6">
            <label class="form-label">部員を選択</label>
            <select v-model="selectedUserId" class="form-select">
              <option disabled value="">部員を選択してください</option>
              <option
                v-for="member in members"
                :key="member.user_id"
                :value="member.user_id"
              >
                {{ member.grade }}年 {{ member.name }}
              </option>
            </select>
          </div>
          <div class="col-md-3">
            <button
              class="btn btn-primary w-100"
              @click="fetchAdvice"
              :disabled="!selectedUserId || loading"
            >
              <span v-if="loading">生成中...</span>
              <span v-else>アドバイスを取得</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- エラー -->
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>

    <!-- アドバイス表示 -->
    <div v-if="adviceHtml" class="card shadow-sm">
      <div class="card-header">{{ selectedMemberName }} へのAIアドバイス</div>
      <div class="card-body prose" v-html="adviceHtml"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { marked } from "marked";
import { getUsers } from "@/services/userService";
import { getAdvice } from "@/services/adviceService";

const members = ref([]);
const selectedUserId = ref("");
const loading = ref(false);
const errorMessage = ref("");
const adviceHtml = ref("");

const selectedMemberName = computed(() => {
  const member = members.value.find((m) => m.user_id === selectedUserId.value);
  return member ? `${member.grade}年 ${member.name}` : "";
});

onMounted(async () => {
  const res = await getUsers("member");
  members.value = res.data.users.filter((m) => m.status === "active");
});

const fetchAdvice = async () => {
  loading.value = true;
  errorMessage.value = "";
  adviceHtml.value = "";

  try {
    const res = await getAdvice(selectedUserId.value);
    adviceHtml.value = marked(res.data.advice);
  } catch (error) {
    if (error.response?.status === 404) {
      errorMessage.value = error.response.data.detail;
    } else if (error.response?.status === 429) {
      errorMessage.value =
        "AIの利用制限に達しました。しばらくしてから再試行してください。";
    } else {
      errorMessage.value = "アドバイスの取得に失敗しました。";
    }
  } finally {
    loading.value = false;
  }
};
</script>
