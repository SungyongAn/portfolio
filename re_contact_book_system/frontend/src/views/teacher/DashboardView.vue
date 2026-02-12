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
              ようこそ、{{ userName }}さん{{ assignmentLabel }}
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
import { useAuthStore } from '@/stores/auth'

const assignmentLabelMap = {
  homeroom: '担任',
  sub_homeroom: '副担任',
}

const authStore = useAuthStore()

const userName = computed(() => authStore.userName)

const primaryAssignment = computed(
  () => authStore.primary_assignment || null
)

const assignmentLabel = computed(() => {
  const type = primaryAssignment.value?.assignment_type
  return assignmentLabelMap[type] ?? ''
})


// 担任または副担任かどうか
const isClassTeacher = computed(() => {
  const type = primaryAssignment.value?.assignment_type
  console.log('[TeacherDashboard] assignment_type:', type)
  return type === 'homeroom' || type === 'sub_homeroom'
})

</script>
