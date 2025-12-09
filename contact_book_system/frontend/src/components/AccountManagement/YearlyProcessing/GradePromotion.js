const GradePromotion = {
  emits: ["updateTitle", "back-to-yearly"],

  data() {
    return {
      isLoading: true,
      isAutoMode: false,
      lastRunDate: null,
      message: "",
    };
  },

  mounted() {
    this.$emit("updateTitle", {
      title: "学年繰り上げ",
      icon: "fas fa-level-up-alt",
      showBackButton: true,
    });

    this.fetchStatus();
  },

  beforeUnmount() {
    this.$emit("updateTitle", { title: "", icon: "", showBackButton: false });
  },

  methods: {
    async fetchStatus() {
      this.isLoading = true;
      try {
        const res = await axios.get("/api/yearly/grade_promotion/status");
        this.isAutoMode = res.data.auto_mode;
        this.lastRunDate = res.data.last_run;
      } catch (error) {
        console.error("エラー:", error);
        this.message = "状態の取得に失敗しました";
      }
      this.isLoading = false;
    },

    async runPromotion() {
      if (!confirm("学年繰り上げを実行しますか？\nこの操作は元に戻せません。"))
        return;

      this.isLoading = true;
      this.message = "";

      try {
        const res = await axios.post("/api/yearly/grade_promotion/run");
        this.message =
          res.data.message || "学年繰り上げが正常に実行されました。";
        this.fetchStatus();
      } catch (error) {
        this.message = "学年繰り上げの実行に失敗しました。";
      }

      this.isLoading = false;
    },

    backToMenu() {
      this.$emit("back-to-yearly");
    },
  },

  template: `
    <div class="container mt-4">
      <div class="row justify-content-center">
        <div class="col-lg-8 col-xl-6">

          <!-- 状態表示 -->
          <div class="card shadow-sm mb-3">
            <div class="card-body">

              <h5 class="mb-3">現在の状態</h5>

              <div v-if="isLoading" class="text-center">
                <div class="spinner-border text-primary"></div>
              </div>

              <div v-else>
                <p><strong>自動モード:</strong>
                  <span v-if="isAutoMode" class="text-success">有効</span>
                  <span v-else class="text-danger">無効</span>
                </p>

                <p><strong>最終実行日:</strong>
                  <span v-if="lastRunDate">{{ lastRunDate }}</span>
                  <span v-else class="text-muted">未実行</span>
                </p>
              </div>

            </div>
          </div>

          <!-- 手動実行 -->
          <div class="card shadow-sm mb-3">
            <div class="card-body text-center">

              <h5 class="mb-3">手動実行</h5>

              <button class="btn btn-primary px-4"
                      :disabled="isLoading"
                      @click="runPromotion">
                <i class="fas fa-play me-1"></i>
                手動で実行する
              </button>

              <p class="text-danger mt-3" v-if="message">{{ message }}</p>

            </div>
          </div>

          <!-- 戻る -->
          <div class="text-center">
            <button class="btn btn-outline-secondary" @click="backToMenu">
              <i class="fas fa-arrow-left me-2"></i>年度処理メニューに戻る
            </button>
          </div>

        </div>
      </div>
    </div>
  `,
};
