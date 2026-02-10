<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-12">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="card-title">
              <i class="bi bi-house-door"></i>
              教師ダッシュボード
            </h1>
            <p class="card-text">
              ようこそ、{{ userName }}さん{{ userRole }}
            </p>
            <hr>
            
            <div class="d-grid gap-2" v-if="isClassTeacher">
              <router-link to="/teacher/submissions" class="btn btn-primary">
                <i class="bi bi-journal-check"></i>
                提出状況
              </router-link>
              <router-link to="/teacher/unread" class="btn btn-warning">
                <i class="bi bi-envelope-open"></i>
                未読連絡帳
              </router-link>
              <router-link to="/teacher/history" class="btn btn-outline-secondary">
                <i class="bi bi-clock-history"></i>
                過去の連絡帳
              </router-link>
            </div>

            <div v-else class="alert alert-secondary">
              あなたには閲覧権限がありません
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
const userRole = computed(() => authStore.user?.role || '')

// 担任または副担任かどうか
const isClassTeacher = computed(() => 
  primary_assignment.assignment_type === '担任' || primary_assignment.assignment_type === '副担任'
)


</script>
