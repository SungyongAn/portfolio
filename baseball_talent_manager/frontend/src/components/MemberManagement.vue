<template>
  <div class="container mt-4">
    <h2 class="mb-4">部員管理</h2>
    <div class="row g-4">
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5 class="card-title">部員作成</h5>
            <p class="card-text text-muted">
              新しい部員のアカウントを作成します。
            </p>
            <router-link
              :to="`/${role}/members/create`"
              class="btn btn-primary mt-3"
            >
              部員作成へ
            </router-link>
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <div class="card shadow-sm h-100">
          <div class="card-body">
            <h5 class="card-title">部員退部・引退処理</h5>
            <p class="card-text text-muted">
              退部または引退する部員の処理を行います。
            </p>
            <router-link
              :to="`/${role}/members/retire`"
              class="btn btn-outline-primary mt-3"
            >
              退部・引退処理へ
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
</script>
