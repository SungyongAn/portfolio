const YearlyProcessingMenu = {
  emits: ["navigate-yearly", "back-to-menu", "updateTitle"],

  mounted() {
    this.$emit("updateTitle", {
      title: "年度処理",
      icon: "fas fa-calendar-check",
      showBackButton: true,
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
        GradePromotion: "grade-promotion",
        GraduationManagement: "graduation-management",
        ClassReassignment: "class-reassignment",
      };
      this.$emit("navigate-yearly", pageMap[page] || page);
    },
    backToAccountMenu() {
      this.$emit("back-to-menu");
    },
  },

  template: `
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-xl-7">
          <div class="row g-3">

            <!-- 学年繰り上げ -->
            <div class="col-md-6">
              <div class="card h-100 shadow-sm hover-card"
                  @click="navigateTo('GradePromotion')"
                  style="cursor: pointer;">
                <div class="card-body text-center p-4">
                  <i class="fas fa-level-up-alt fa-3x text-primary mb-3"></i>
                  <h5 class="card-title">学年繰り上げ</h5>
                  <p class="card-text text-muted small">
                    自動処理の状態確認・手動実行ができます
                  </p>
                </div>
              </div>
            </div>

            <!-- 卒業処理 -->
            <div class="col-md-6">
              <div class="card h-100 shadow-sm hover-card"
                  @click="navigateTo('GraduationManagement')"
                  style="cursor: pointer;">
                <div class="card-body text-center p-4">
                  <i class="fas fa-user-graduate fa-3x text-success mb-3"></i>
                  <h5 class="card-title">卒業処理</h5>
                  <p class="card-text text-muted small">
                    status=graduated の確認と手動更新
                  </p>
                </div>
              </div>
            </div>

            <!-- クラス替え -->
            <div class="col-md-6">
              <div class="card h-100 shadow-sm hover-card"
                  @click="navigateTo('ClassReassignment')"
                  style="cursor: pointer;">
                <div class="card-body text-center p-4">
                  <i class="fas fa-exchange-alt fa-3x text-warning mb-3"></i>
                  <h5 class="card-title">クラス替え</h5>
                  <p class="card-text text-muted small">
                    CSVを使った一括更新ができます
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
