<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-12">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="card-title">
              <i class="bi bi-house-door"></i>
              生徒ダッシュボード
            </h1>
            <p class="card-text">
              ようこそ、{{ userName }}さん
            </p>
            <hr>
            <div class="alert alert-info">
              <i class="bi bi-info-circle"></i>
              このページは開発中です
            </div>
            <div class="d-grid gap-2">
              <router-link to="/student/submit" class="btn btn-primary">
                <i class="bi bi-pencil-square"></i>
                連絡帳を提出
              </router-link>
              <router-link to="/student/history" class="btn btn-outline-secondary">
                <i class="bi bi-clock-history"></i>
                過去の記録
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const userName = computed(() => authStore.userName)
</script>