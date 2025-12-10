const ArchiveManagement = {
  emits: ["back-to-menu", "updateTitle"],
  data() {
    return {
      statistics: {
        active: null,
        archive: null,
      },
      deletionLogs: [],
      searchResults: [],
      isLoading: false,
      errorMessage: "",
      successMessage: "",

      // 検索フォーム
      searchForm: {
        studentName: "",
        year: new Date().getFullYear(),
        month: null,
      },

      // 実行確認モーダル
      showConfirmModal: false,
      confirmAction: null,
      confirmMessage: "",
    };
  },
  computed: {
    totalRecords() {
      const active = this.statistics.active?.record_count || 0;
      const archive = this.statistics.archive?.record_count || 0;
      return active + archive;
    },
    totalSize() {
      const active = this.statistics.active?.size_mb || 0;
      const archive = this.statistics.archive?.size_mb || 0;
      return (active + archive).toFixed(2);
    },
  },
  async mounted() {
    this.$emit("updateTitle", {
      title: "アーカイブ管理",
      icon: "fas fa-database",
      showBackButton: true,
    });

    await this.loadStatistics();
    await this.loadDeletionLogs();
  },
  beforeUnmount() {
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },
  methods: {
    async loadStatistics() {
      this.isLoading = true;
      this.errorMessage = "";

      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/archive-management/statistics"
        );

        if (response.data.success) {
          const data = response.data.data;
          this.statistics.active = data.find((d) => d.data_type === "active");
          this.statistics.archive = data.find((d) => d.data_type === "archive");
        }
      } catch (err) {
        console.error(err);
        this.errorMessage = "データの読み込みに失敗しました";
      } finally {
        this.isLoading = false;
      }
    },

    async loadDeletionLogs() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/archive-management/deletion-logs",
          { params: { limit: 10 } }
        );

        if (response.data.success) {
          this.deletionLogs = response.data.data;
        }
      } catch (err) {
        console.error(err);
      }
    },

    confirmArchive() {
      this.confirmAction = "archive";
      this.confirmMessage =
        "3年以上前のデータをアーカイブします。よろしいですか？";
      this.showConfirmModal = true;
    },

    confirmDelete() {
      this.confirmAction = "delete";
      this.confirmMessage =
        "5年以上前のデータを完全に削除します。この操作は元に戻せません。よろしいですか？";
      this.showConfirmModal = true;
    },

    async executeConfirmedAction() {
      this.showConfirmModal = false;

      if (this.confirmAction === "archive") {
        await this.executeArchive();
      } else if (this.confirmAction === "delete") {
        await this.executeDelete();
      }
    },

    async executeArchive() {
      this.isLoading = true;
      this.errorMessage = "";
      this.successMessage = "";

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/archive-management/execute-archive",
          { archive_years: 3 }
        );

        if (response.data.success) {
          this.successMessage = response.data.message;
          await this.loadStatistics();
          await this.loadDeletionLogs();
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (err) {
        console.error(err);
        this.errorMessage = "アーカイブの実行に失敗しました";
      } finally {
        this.isLoading = false;
      }
    },

    async executeDelete() {
      this.isLoading = true;
      this.errorMessage = "";
      this.successMessage = "";

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/archive-management/execute-deletion",
          { retention_years: 5 }
        );

        if (response.data.success) {
          this.successMessage = response.data.message;
          await this.loadStatistics();
          await this.loadDeletionLogs();
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (err) {
        console.error(err);
        this.errorMessage = "データ削除の実行に失敗しました";
      } finally {
        this.isLoading = false;
      }
    },

    async searchArchive() {
      this.isLoading = true;
      this.errorMessage = "";
      this.searchResults = [];

      try {
        const params = {};
        if (this.searchForm.studentName) {
          params.student_name = this.searchForm.studentName;
        }
        if (this.searchForm.year) {
          params.year = this.searchForm.year;
        }
        if (this.searchForm.month) {
          params.month = this.searchForm.month;
        }

        const response = await axios.get(
          "http://127.0.0.1:8000/archive-management/search-archive",
          { params }
        );

        if (response.data.success) {
          this.searchResults = response.data.data;
        } else {
          this.errorMessage = response.data.message;
        }
      } catch (err) {
        console.error(err);
        this.errorMessage = "アーカイブ検索に失敗しました";
      } finally {
        this.isLoading = false;
      }
    },

    formatDate(dateString) {
      if (!dateString) return "-";
      return new Date(dateString).toLocaleDateString("ja-JP");
    },

    formatDateTime(dateString) {
      if (!dateString) return "-";
      return new Date(dateString).toLocaleString("ja-JP");
    },
  },
  template: `
<div class="container mt-4">
  <!-- エラー・成功メッセージ -->
  <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
    {{ errorMessage }}
    <button type="button" class="btn-close" @click="errorMessage = ''"></button>
  </div>
  
  <div v-if="successMessage" class="alert alert-success alert-dismissible fade show">
    {{ successMessage }}
    <button type="button" class="btn-close" @click="successMessage = ''"></button>
  </div>

  <!-- 統計情報 -->
  <div class="row mb-4">
    <div class="col-md-12">
      <div class="card">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0"><i class="fas fa-chart-bar me-2"></i>データ保管状況</h5>
        </div>
        <div class="card-body">
          <div class="row">
            <!-- アクティブデータ -->
            <div class="col-md-4">
              <div class="card bg-light">
                <div class="card-body">
                  <h6 class="card-title">アクティブデータ（0-3年）</h6>
                  <p class="fs-3 mb-1">{{ statistics.active?.record_count?.toLocaleString() || 0 }}件</p>
                  <p class="text-muted mb-1">{{ statistics.active?.size_mb || 0 }} MB</p>
                  <small class="text-muted">
                    {{ formatDate(statistics.active?.oldest_date) }} 〜 {{ formatDate(statistics.active?.newest_date) }}
                  </small>
                </div>
              </div>
            </div>
            
            <!-- アーカイブデータ -->
            <div class="col-md-4">
              <div class="card bg-light">
                <div class="card-body">
                  <h6 class="card-title">アーカイブデータ（3-5年）</h6>
                  <p class="fs-3 mb-1">{{ statistics.archive?.record_count?.toLocaleString() || 0 }}件</p>
                  <p class="text-muted mb-1">{{ statistics.archive?.size_mb || 0 }} MB</p>
                  <small class="text-muted">
                    {{ formatDate(statistics.archive?.oldest_date) }} 〜 {{ formatDate(statistics.archive?.newest_date) }}
                  </small>
                </div>
              </div>
            </div>
            
            <!-- 合計 -->
            <div class="col-md-4">
              <div class="card bg-info text-white">
                <div class="card-body">
                  <h6 class="card-title">合計</h6>
                  <p class="fs-3 mb-1">{{ totalRecords.toLocaleString() }}件</p>
                  <p class="mb-1">{{ totalSize }} MB</p>
                  <small>
                    次回自動実行: 2026年4月1日
                  </small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- アクションボタン -->
  <div class="row mb-4">
    <div class="col-md-12">
      <div class="card">
        <div class="card-header bg-secondary text-white">
          <h5 class="mb-0"><i class="fas fa-cogs me-2"></i>手動実行</h5>
        </div>
        <div class="card-body">
          <div class="d-flex gap-3 flex-wrap">
            <button 
              class="btn btn-primary btn-lg" 
              @click="confirmArchive"
              :disabled="isLoading">
              <i class="fas fa-archive me-2"></i>アーカイブ実行
            </button>
            
            <button 
              class="btn btn-danger btn-lg" 
              @click="confirmDelete"
              :disabled="isLoading">
              <i class="fas fa-trash me-2"></i>古いデータを削除
            </button>
            
            <button 
              class="btn btn-outline-secondary btn-lg" 
              @click="loadStatistics"
              :disabled="isLoading">
              <i class="fas fa-sync me-2"></i>更新
            </button>
          </div>
          
          <div class="mt-3">
            <small class="text-muted">
              <i class="fas fa-info-circle me-1"></i>
              アーカイブ: 3年以上前のデータを圧縮保管します（検索可能）<br>
              <i class="fas fa-exclamation-triangle me-1 text-danger"></i>
              削除: 5年以上前のデータを完全に削除します（元に戻せません）
            </small>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- アーカイブ検索 -->
  <div class="row mb-4">
    <div class="col-md-12">
      <div class="card">
        <div class="card-header bg-success text-white">
          <h5 class="mb-0"><i class="fas fa-search me-2"></i>アーカイブ検索</h5>
        </div>
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-4">
              <label class="form-label">生徒名</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="searchForm.studentName"
                placeholder="部分一致検索">
            </div>
            
            <div class="col-md-3">
              <label class="form-label">年</label>
              <input 
                type="number" 
                class="form-control" 
                v-model.number="searchForm.year"
                :min="2020"
                :max="new Date().getFullYear()">
            </div>
            
            <div class="col-md-3">
              <label class="form-label">月</label>
              <select class="form-select" v-model.number="searchForm.month">
                <option :value="null">すべて</option>
                <option v-for="m in 12" :key="m" :value="m">{{ m }}月</option>
              </select>
            </div>
            
            <div class="col-md-2 d-flex align-items-end">
              <button 
                class="btn btn-success w-100" 
                @click="searchArchive"
                :disabled="isLoading">
                <i class="fas fa-search me-2"></i>検索
              </button>
            </div>
          </div>
          
          <!-- 検索結果 -->
          <div v-if="searchResults.length > 0" class="mt-4">
            <h6>検索結果: {{ searchResults.length }}件</h6>
            <div class="table-responsive">
              <table class="table table-striped">
                <thead>
                  <tr>
                    <th>生徒名</th>
                    <th>学年・クラス</th>
                    <th>対象日</th>
                    <th>体調</th>
                    <th>メンタル</th>
                    <th>振り返り</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(result, index) in searchResults" :key="index">
                    <td>{{ result.student_name }}</td>
                    <td>{{ result.grade }}年{{ result.class_name }}組</td>
                    <td>{{ formatDate(result.target_date) }}</td>
                    <td>{{ result.physical_condition }}/5</td>
                    <td>{{ result.mental_state }}/5</td>
                    <td>{{ result.daily_reflection.substring(0, 50) }}...</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div v-else-if="searchResults.length === 0 && !isLoading" class="alert alert-info mt-3">
            検索条件を指定して検索してください
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 削除ログ -->
  <div class="row mb-4">
    <div class="col-md-12">
      <div class="card">
        <div class="card-header bg-warning">
          <h5 class="mb-0"><i class="fas fa-history me-2"></i>削除履歴</h5>
        </div>
        <div class="card-body">
          <div v-if="deletionLogs.length > 0" class="table-responsive">
            <table class="table table-sm">
              <thead>
                <tr>
                  <th>実行日時</th>
                  <th>対象テーブル</th>
                  <th>削除件数</th>
                  <th>対象期間</th>
                  <th>理由</th>
                  <th>実行者</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in deletionLogs" :key="log.id">
                  <td>{{ formatDateTime(log.deletion_date) }}</td>
                  <td>{{ log.table_name }}</td>
                  <td>{{ log.records_deleted.toLocaleString() }}件</td>
                  <td>〜{{ formatDate(log.date_range_to) }}</td>
                  <td>{{ log.reason }}</td>
                  <td>{{ log.executed_by }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="alert alert-info">
            削除履歴はありません
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- 確認モーダル -->
  <div v-if="showConfirmModal" class="modal d-block" tabindex="-1" style="background: rgba(0,0,0,0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">確認</h5>
          <button type="button" class="btn-close" @click="showConfirmModal = false"></button>
        </div>
        <div class="modal-body">
          <p>{{ confirmMessage }}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="showConfirmModal = false">
            キャンセル
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="executeConfirmedAction">
            実行
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ローディング -->
  <div v-if="isLoading" class="position-fixed top-50 start-50 translate-middle">
    <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</div>
`,
};
