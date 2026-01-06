<template>
  <div class="container mt-5">
    <div class="card shadow">
      <div class="card-body">
        <h1><i class="bi bi-gear"></i> 管理者ダッシュボード</h1>
        <p>ようこそ、{{ userName }}さん</p>
        <button @click="handleLogout" class="btn btn-outline-danger">
          <i class="bi bi-box-arrow-right"></i> ログアウト
        </button>
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

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>