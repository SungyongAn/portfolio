<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-8 col-xl-7">
        <div class="row g-3">
          <!-- アカウント作成カード -->
          <div class="col-md-6">
            <div
              class="card h-100 shadow-sm hover-card"
              @click="navigateTo('account-form')"
              style="cursor: pointer"
            >
              <div class="card-body text-center p-4">
                <i class="fas fa-user-plus fa-3x text-success mb-3"></i>
                <h5 class="card-title">アカウント作成</h5>
                <p class="card-text text-muted small">
                  新しい生徒または教師のアカウントを作成します
                </p>
              </div>
            </div>
          </div>

          <!-- アカウント検索カード -->
          <div class="col-md-6">
            <div
              class="card h-100 shadow-sm hover-card"
              @click="navigateTo('account-search')"
              style="cursor: pointer"
            >
              <div class="card-body text-center p-4">
                <i class="fas fa-search fa-3x text-primary mb-3"></i>
                <h5 class="card-title">アカウント情報の変更</h5>
                <p class="card-text text-muted small">
                  既存のアカウントを検索・情報の変更を行えます
                </p>
              </div>
            </div>
          </div>

          <!-- アーカイブ管理カード -->
          <div class="col-md-6">
            <div
              class="card h-100 shadow-sm hover-card"
              @click="navigateTo('archive-management')"
              style="cursor: pointer"
            >
              <div class="card-body text-center p-4">
                <i class="fas fa-database fa-3x text-warning mb-3"></i>
                <h5 class="card-title">アーカイブ管理</h5>
                <p class="card-text text-muted small">
                  データの保管状況とアーカイブ設定
                </p>
              </div>
            </div>
          </div>

          <!-- 年度処理カード -->
          <div class="col-md-6">
            <div
              class="card h-100 shadow-sm hover-card"
              @click="navigateTo('yearly-processing-menu')"
              style="cursor: pointer"
            >
              <div class="card-body text-center p-4">
                <i class="fas fa-calendar-alt fa-3x text-warning mb-3"></i>
                <h5 class="card-title">年次処理</h5>
                <p class="card-text text-muted small"></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "AccountManagementMenu",
  emits: ["updateTitle"],
  setup() {
    const router = useRouter();
    const navigateTo = (routeName) => {
      console.log("🔍 navigateTo called with:", routeName);
      console.log("📋 Current route:", router.currentRoute.value.path);

      router
        .push({ name: routeName })
        .then(() => {
          console.log(
            "✅ Navigation successful to:",
            router.currentRoute.value.path
          );
        })
        .catch((error) => {
          console.error("❌ Navigation error:", error);
        });
    };
    return { navigateTo };
  },
  mounted() {
    console.log("🎬 AccountManagementMenu mounted");
    this.$emit("updateTitle", {
      title: "アカウント管理",
      icon: "fas fa-users-cog",
      showBackButton: false,
    });
  },
  beforeUnmount() {
    console.log("👋 AccountManagementMenu unmounting");
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },
};
</script>
