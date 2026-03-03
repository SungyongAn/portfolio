<template>
  <div class="container mt-4">
    <h2 class="mb-4">ダッシュボード</h2>

    <div class="row g-4">
      <!-- 測定確認 / 承認 -->
      <div v-if="isMember || isCoach" class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>測定結果の確認 / 承認</h5>
            <router-link :to="`/${role}/review`" class="btn btn-primary mt-3">
              測定結果の確認
            </router-link>
          </div>
        </div>
      </div>

      <!-- 測定記録閲覧 -->
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>測定記録の閲覧</h5>
            <router-link
              :to="`/${role}/history`"
              class="btn btn-outline-primary mt-3"
            >
              測定記録一覧を見る
            </router-link>
          </div>
        </div>
      </div>

      <!-- 部員管理 -->
      <div v-if="isCoach || isDirector" class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5>部員の管理</h5>
            <router-link :to="`/${role}/members`" class="btn btn-warning mt-3">
              管理画面へ
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore();

const role = computed(() => authStore.role);
const isMember = computed(() => authStore.isMember);
const isCoach = computed(() => authStore.isCoach);
const isDirector = computed(() => authStore.isDirector);
</script>
