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
            <li v-for="item in menuItems" :key="item.to" class="nav-item">
              <router-link :to="item.to" class="nav-link" active-class="active">
                <i :class="`bi ${item.icon}`"></i>
                {{ item.label }}
              </router-link>
            </li>
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
import { computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const router = useRouter();
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

// ロール別メニュー定義
const menuMap = {
  manager: [
    { label: "ダッシュボード", to: "/manager/dashboard", icon: "bi-house" },
    { label: "測定結果の入力", to: "/manager/record", icon: "bi-pencil" },
    { label: "ステータス確認", to: "/manager/status", icon: "bi-list-check" },
  ],
  member: [
    { label: "ダッシュボード", to: "/member/dashboard", icon: "bi-house" },
    { label: "測定結果の確認", to: "/member/review", icon: "bi-check-circle" },
    {
      label: "測定記録の閲覧",
      to: "/member/history",
      icon: "bi-clock-history",
    },
  ],
  coach: [
    { label: "ダッシュボード", to: "/coach/dashboard", icon: "bi-house" },
    { label: "測定結果の承認", to: "/coach/review", icon: "bi-check-circle" },
    { label: "測定記録の閲覧", to: "/coach/history", icon: "bi-clock-history" },
    { label: "部員管理", to: "/coach/members", icon: "bi-people" },
  ],
  director: [
    { label: "ダッシュボード", to: "/director/dashboard", icon: "bi-house" },
    {
      label: "測定記録の閲覧",
      to: "/director/history",
      icon: "bi-clock-history",
    },
    { label: "部員管理", to: "/director/members", icon: "bi-people" },
  ],
};

// ロールに応じた表示メニュー
const menuItems = computed(() => {
  return menuMap[role.value] || [];
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
    router.push("/login");
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
