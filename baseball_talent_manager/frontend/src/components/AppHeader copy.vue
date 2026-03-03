<template>
  <header class="app-header">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <!-- ロゴ・アプリ名 -->
        <router-link to="/" class="navbar-brand">
          <i class="bi bi-journal-text me-2"></i>
          野球部タレントマネジメントシステム
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
            <template v-if="role === 'manager'">
              <li class="nav-item">
                <router-link
                  to="/manager/dashboard"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-house-door"></i>
                  ダッシュボード
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/manager/record"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-pencil-square"></i>
                  測定結果の入力
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/manager/status"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-clock-history"></i>
                  承認依頼中のステータス確認
                </router-link>
              </li>
            </template>

            <template v-else-if="role === 'member'">
              <li class="nav-item">
                <router-link
                  to="/member/dashboard"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-house-door"></i>
                  ダッシュボード
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/member/review"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-list-check"></i>
                  測定結果の確認と承認
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/member/history"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-envelope"></i>
                  測定記録の閲覧
                  <span v-if="unreadCount > 0" class="badge bg-danger ms-1">
                    {{ unreadCount }}
                  </span>
                </router-link>
              </li>
            </template>

            <template v-else-if="role === 'coach'">
              <li class="nav-item">
                <router-link
                  to="/coach/dashboard"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-people"></i>
                  ダッシュボード
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/coach/review"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-building"></i>
                  測定結果の確認と承認
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/coach/history"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-building"></i>
                  測定記録の閲覧
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/coach/members/create"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-building"></i>
                  部員作成
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/coach/members/retire"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-building"></i>
                  部員退部・引退処理
                </router-link>
              </li>
            </template>

            <template v-else-if="role === 'director'">
              <li class="nav-item">
                <router-link
                  to="/director/dashboard"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-people"></i>
                  ダッシュボード
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/director/history"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-building"></i>
                  測定記録の閲覧
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/director/members/create"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-building"></i>
                  部員作成
                </router-link>
              </li>
              <li class="nav-item">
                <router-link
                  to="/director/members/retire"
                  class="nav-link"
                  active-class="active"
                >
                  <i class="bi bi-building"></i>
                  部員退部・引退処理
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
import { computed, ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

// ユーザー情報
const userName = computed(() => authStore.userName || "ゲスト");
const role = computed(() => authStore.role);

// クラス情報（Storeから取得）
const classInfo = computed(() => {
  if (authStore.isManager || authStore.isMember) {
    if (!authStore.memberGrade) return null;
    return `${authStore.memberGrade}年`;
  }
  return null;
});

// ロールアイコン
const getRoleIcon = computed(() => {
  const icons = {
    manager: "bi bi-clipboard-data",
    member: "bi bi-person",
    coach: "bi bi-people",
    director: "bi bi-award",
  };
  return icons[role.value] || "bi bi-person";
});

// 現在のページ名
const currentPageName = computed(() => {
  return route.meta.title || "ページ";
});

// パンくずリスト
const breadcrumbs = computed(() => {
  return route.meta.breadcrumbs || [];
});

const showBreadcrumb = computed(() => {
  return breadcrumbs.value.length > 0;
});

// ログアウト
const handleLogout = async () => {
  if (confirm("ログアウトしてもよろしいですか？")) {
    await authStore.logout();
  }
};
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
