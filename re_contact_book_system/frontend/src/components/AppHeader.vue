<template>
  <header class="app-header">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <!-- ロゴ・アプリ名 -->
        <router-link to="/" class="navbar-brand">
          <i class="bi bi-journal-text me-2"></i>
          連絡帳システム
        </router-link>

        <!-- モバイル用トグルボタン -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarContent"
          aria-controls="navbarContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarContent">
          <!-- 左側：ナビゲーション -->
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <!-- ロール別メニュー -->
            <template v-if="role === 'student'">
              <li class="nav-item">
                <router-link to="/student/dashboard" class="nav-link" active-class="active">
                  <i class="bi bi-house-door"></i>
                  ダッシュボード
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/student/submit" class="nav-link" active-class="active">
                  <i class="bi bi-pencil-square"></i>
                  連絡帳提出
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/student/history" class="nav-link" active-class="active">
                  <i class="bi bi-clock-history"></i>
                  履歴
                </router-link>
              </li>
            </template>

            <template v-else-if="role === 'teacher'">
              <li class="nav-item">
                <router-link to="/teacher/dashboard" class="nav-link" active-class="active">
                  <i class="bi bi-house-door"></i>
                  ダッシュボード
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/teacher/submissions" class="nav-link" active-class="active">
                  <i class="bi bi-list-check"></i>
                  提出状況
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/teacher/unread" class="nav-link" active-class="active">
                  <i class="bi bi-envelope"></i>
                  未読
                  <span v-if="unreadCount > 0" class="badge bg-danger ms-1">
                    {{ unreadCount }}
                  </span>
                </router-link>
              </li>
            </template>

            <!-- メニュー -->
            <template v-else-if="role === 'admin'">
              <li class="nav-item">
                <router-link to="/admin/users" class="nav-link" active-class="active">
                  <i class="bi bi-people"></i>
                  ユーザー管理
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/grades" class="nav-link" active-class="active">
                  <i class="bi bi-building"></i>
                  学年・クラス管理
                </router-link>
              </li>
            </template>
          </ul>

          <!-- 右側：ユーザー情報とログアウト -->
          <div class="d-flex align-items-center">
            <!-- パンくずリスト（現在のページ） -->
            <span class="navbar-text me-3 d-none d-lg-block">
              <i class="bi bi-geo-alt"></i>
              {{ currentPageName }}
            </span>

            <div class="d-flex align-items-center">
          <!-- ユーザー名表示 -->
          <span class="text-white me-3">
            <i :class="getRoleIcon"></i>
            {{ userName }}
            <span v-if="classInfo" class="ms-2 text-white-50">
              ({{ classInfo }})
            </span>
          </span>

          <!-- ✅ シンプルなログアウトボタン -->
          <button 
            @click="handleLogout" 
            class="btn btn-outline-light btn-sm"
          >
            <i class="bi bi-box-arrow-right"></i>
            ログアウト
          </button>
        </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- サブヘッダー（パンくずリスト詳細版 - オプション） -->
    <div v-if="showBreadcrumb" class="bg-light border-bottom py-2">
      <div class="container-fluid">
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb mb-0">
            <li class="breadcrumb-item">
              <router-link to="/">ホーム</router-link>
            </li>
            <li
              v-for="(crumb, index) in breadcrumbs"
              :key="index"
              class="breadcrumb-item"
              :class="{ active: index === breadcrumbs.length - 1 }"
            >
              <router-link v-if="crumb.to" :to="crumb.to">
                {{ crumb.name }}
              </router-link>
              <span v-else>{{ crumb.name }}</span>
            </li>
          </ol>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// ユーザー情報
const userName = computed(() => authStore.userName || 'ゲスト')
const role = computed(() => authStore.role)
const grade_number = computed(() =>
  isStudent.value ? authStore.student_class?.grade_number : null
)

const class_name = computed(() =>
  isStudent.value ? authStore.student_class?.class_name : null
)
const userId = computed(() => authStore.userId)


// クラス情報（Storeから取得 - 将来実装）
const classInfo = computed(() => {
  if (authStore.isStudent) {
    if (!authStore.studentGrade || !authStore.studentClassName) return null
    return `${authStore.studentGrade}年${authStore.studentClassName}`
  }

  if (authStore.isTeacher) {
    // 例：担任が最初の assignment と仮定
    const assignment = authStore.teacherAssignments[0]
    if (!assignment) return null

    return `${assignment.grade_number}年${assignment.class_name} 担任`
  }

  return null
})

// 未読件数（教師のみ）
const unreadCount = ref(0)
// TODO: 定期的にAPIから未読件数を取得

// ユーザーイニシャル
const userInitial = computed(() => {
  if (!userName.value) return '?'
  return userName.value.charAt(0).toUpperCase()
})

// ロールアイコン
const getRoleIcon = computed(() => {
  const icons = {
    student: 'bi bi-person',
    teacher: 'bi bi-person-badge',
    admin: 'bi bi-gear'
  }
  return icons[role.value] || 'bi bi-person'
})

// ロールラベル
const getRoleLabel = computed(() => {
  const labels = {
    student: '生徒',
    teacher: '教師',
    admin: '管理者'
  }
  return labels[role.value] || role.value
})

// 現在のページ名
const currentPageName = computed(() => {
  return route.meta.title || 'ページ'
})

// パンくずリスト
const breadcrumbs = computed(() => {
  return route.meta.breadcrumbs || []
})

const showBreadcrumb = computed(() => {
  return breadcrumbs.value.length > 0
})

// ログアウト
const handleLogout = () => {
  if (confirm('ログアウトしてもよろしいですか？')) {
    authStore.logout()
    router.push('/login')
  }
}

// 未読件数の定期取得（教師のみ）
if (role.value === 'teacher') {
  // TODO: 定期的に未読件数を取得
  // setInterval(() => {
  //   fetchUnreadCount()
  // }, 60000) // 1分ごと
}
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 1030;
}

.navbar-brand {
  font-weight: 600;
  font-size: 1.25rem;
}

.nav-link {
  transition: all 0.2s;
  border-radius: 0.25rem;
  margin: 0 0.25rem;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 500;
}

.dropdown-item-text {
  min-width: 280px;
}

.avatar {
  font-size: 1.2rem;
  font-weight: 600;
}

.breadcrumb {
  font-size: 0.875rem;
}

.breadcrumb-item a {
  text-decoration: none;
  color: #0d6efd;
}

.breadcrumb-item a:hover {
  text-decoration: underline;
}
</style>