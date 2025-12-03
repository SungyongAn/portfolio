const AccountManagementMenu = {
  emits: ["navigate-account", "back-to-menu", "updateTitle"],
  mounted() {
    this.$emit("updateTitle", {
      title: "アカウント管理",
      icon: "fas fa-users-cog",
      showBackButton: false,
    });
  },
  beforeUnmount() {
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },
  methods: {
    navigateTo(page) {
      const pageMap = {
        AccountForm: "account-form",
        AccountSearch: "account-search",
        ArchiveManagement: "archive-management",
      };
      this.$emit("navigate-account", pageMap[page] || page);
    },
  },
  template: `
        <div class="container mt-4">
            <div class="row justify-content-center">
                <div class="col-lg-8 col-xl-7">
                    <div class="row g-3">
                        <!-- アカウント作成カード -->
                        <div class="col-md-6">
                            <div class="card h-100 shadow-sm hover-card" 
                                @click="navigateTo('AccountForm')" 
                                style="cursor: pointer;">
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
                            <div class="card h-100 shadow-sm hover-card" 
                                @click="navigateTo('AccountSearch')" 
                                style="cursor: pointer;">
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
                            <div class="card h-100 shadow-sm hover-card" 
                                @click="navigateTo('ArchiveManagement')" 
                                style="cursor: pointer;">
                                <div class="card-body text-center p-4">
                                    <i class="fas fa-database fa-3x text-warning mb-3"></i>
                                    <h5 class="card-title">アーカイブ管理</h5>
                                    <p class="card-text text-muted small">
                                        データの保管状況とアーカイブ設定
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
};
