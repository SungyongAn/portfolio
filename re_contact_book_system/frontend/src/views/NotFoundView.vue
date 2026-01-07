<template>
  <div class="container mt-5 text-center">
    <h1 class="display-1">404</h1>
    <p class="lead">ページが見つかりません</p>
    <button @click="goToDashboard" class="btn btn-primary me-2">
      ダッシュボードへ
    </button>
    <button @click="handleLogout" class="btn btn-secondary">
      ログアウト
    </button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const goToDashboard = () => {
  const role = authStore.role
  router.push(`/${role}/dashboard`)
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>