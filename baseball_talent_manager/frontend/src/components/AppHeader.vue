<template>
  <header class="sticky-top">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
      <div class="container-fluid">
        <!-- ロゴ・アプリ名 -->
        <router-link to="/" class="navbar-brand fw-semibold">
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
            <li v-for="item in menuItems" :key="item.to" class="nav-item">
              <router-link :to="item.to" class="nav-link" active-class="active">
                <i :class="`bi ${item.icon}`"></i>
                {{ item.label }}
              </router-link>
            </li>
          </ul>

          <!-- 右側：ユーザー情報とログアウト -->
          <div class="d-flex align-items-center">
            <div class="d-flex align-items-center">
              <!-- ユーザー名表示 -->
              <span class="text-white me-3">
                <i :class="getRoleIcon"></i>
                {{ userName }}
                <span v-if="classInfo" class="ms-2 text-white-50">
                  ({{ classInfo }})
                </span>
              </span>

              <!-- ログアウトボタン -->
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
  </header>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const authStore = useAuthStore();

// ユーザー情報
const userName = computed(() => authStore.userName || "ゲスト");
const role = computed(() => authStore.role);

// クラス情報
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

// ロール別メニュー
const menuMap = {
  manager: [
    { label: "ダッシュボード", to: "/manager/dashboard", icon: "bi-house" },
    { label: "測定結果の入力", to: "/manager/record", icon: "bi-pencil" },
    { label: "ステータス確認", to: "/manager/status", icon: "bi-list-check" },
    { label: "測定登録状況", to: "/manager/progress", icon: "bi-bar-chart" },
  ],
  member: [
    { label: "ダッシュボード", to: "/member/dashboard", icon: "bi-house" },
    { label: "測定結果の確認", to: "/member/review", icon: "bi-check-circle" },
    {
      label: "測定記録の閲覧",
      to: "/member/history",
      icon: "bi-clock-history",
    },
    { label: "可視化ダッシュボード", to: "/member/chart", icon: "bi-graph-up" },
  ],
  coach: [
    { label: "ダッシュボード", to: "/coach/dashboard", icon: "bi-house" },
    { label: "測定結果の承認", to: "/coach/review", icon: "bi-check-circle" },
    { label: "測定記録の閲覧", to: "/coach/history", icon: "bi-clock-history" },
    { label: "測定登録状況", to: "/coach/progress", icon: "bi-bar-chart" },
    { label: "可視化ダッシュボード", to: "/coach/chart", icon: "bi-graph-up" },
    { label: "部員管理", to: "/coach/members", icon: "bi-people" },
    { label: "AIアドバイス", to: "/coach/advice", icon: "bi-robot" },
  ],
  director: [
    { label: "ダッシュボード", to: "/director/dashboard", icon: "bi-house" },
    {
      label: "測定記録の閲覧",
      to: "/director/history",
      icon: "bi-clock-history",
    },
    { label: "測定登録状況", to: "/director/progress", icon: "bi-bar-chart" },
    {
      label: "可視化ダッシュボード",
      to: "/director/chart",
      icon: "bi-graph-up",
    },
    { label: "部員管理", to: "/director/members", icon: "bi-people" },
    { label: "AIアドバイス", to: "/director/advice", icon: "bi-robot" },
  ],
};

const menuItems = computed(() => menuMap[role.value] || []);

// ログアウト
const handleLogout = async () => {
  if (confirm("ログアウトしてもよろしいですか？")) {
    await authStore.logout();
    router.push("/login");
  }
};
</script>
