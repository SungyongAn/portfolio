// 担任・副担任）過去の連絡帳閲覧
const ClassPastRenrakucho = {
  props: ['currentUser'],
  emits: ['back', 'updateTitle'],
  data() {
    const today = new Date();
    return {
      selectedYear: today.getFullYear(),
      selectedMonth: today.getMonth() + 1,
      selectedDay: null,
      selectedWeekday: null,
      studentName: '',
      records: [],
      isLoading: false,
      message: '',
      currentPage: 1,
      perPage: 10,
      selectedRecord: null,
      showModal: false
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.records.length / this.perPage) || 1;
    },
    paginatedRecords() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.records.slice(start, end);
    },
    isTeacher() {
      return this.currentUser?.role === 'teacher' || this.currentUser?.role === '教師';
    },
    isAdmin() {
      return this.currentUser?.role === 'admin' || this.currentUser?.role === '管理者';
    }
  },
  mounted() {
    // ヘッダーにタイトルと戻るボタンを設定
    this.$emit('updateTitle', {
      title: '連絡帳履歴',
      icon: 'fas fa-folder-open',
      showBackButton: true
    });
  },
  beforeUnmount() {
    // コンポーネント離脱時にタイトルをクリア
    this.$emit('updateTitle', {
      title: '',
      icon: '',
      showBackButton: false
    });
  },
  methods: {
    async fetchClassPastRecords() {
      if (!this.currentUser) return;

      this.isLoading = true;
      this.message = '';
      this.records = [];
      this.currentPage = 1;

      const payload = {
        grade: Number(this.currentUser.grade),
        class_name: this.currentUser.className,
        teacher_name: this.currentUser.fullName,
        student_name: this.studentName || null,
        year: Number(this.selectedYear),
        month: Number(this.selectedMonth)
      };
      if (this.selectedDay) payload.day = Number(this.selectedDay);
      if (this.selectedWeekday !== null) payload.weekday = Number(this.selectedWeekday);
      payload.flag = true;

      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/renrakucho-management/past-renrakucho-search',
          payload,
          { headers: { 'Content-Type': 'application/json' } }
        );
        this.records = response.data.data || [];
        if (!this.records.length) this.message = '検索条件に一致するデータがありません';
      } catch (error) {
        console.error(error);
        this.message = error.response?.data?.detail || '連絡帳データの取得に失敗しました';
      } finally {
        this.isLoading = false;
      }
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    formatDate(dateStr) {
      if (!dateStr) return '-';
      const d = new Date(dateStr);
      return `${d.getMonth() + 1}/${d.getDate()}`;
    },
    formatDateFull(dateStr) {
      if (!dateStr) return '-';
      const d = new Date(dateStr);
      return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
    },
    showDetail(record) {
      this.selectedRecord = record;
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.selectedRecord = null;
    },
    resetFilters() {
      this.selectedDay = null;
      this.selectedWeekday = null;
      this.studentName = '';
    }
  },
  template: `
    <div class="container-fluid mt-4 px-2">
      <div class="row">

        <!-- 左サイドバー: 検索条件 -->
        <div class="col-12 col-md-3 mb-3">
          <div class="card h-100">
            <div class="card-header bg-primary text-white">
              <h5 class="mb-0">
                <i class="fas fa-filter me-2"></i>検索条件
              </h5>
            </div>
            <div class="card-body">

              <!-- 生徒名 -->
              <div class="mb-3">
                <label class="form-label fw-bold">
                  <i class="fas fa-user me-1"></i>生徒名
                </label>
                <input 
                  v-model="studentName" 
                  type="text" 
                  class="form-control" 
                  placeholder="生徒名を入力"
                >
              </div>

              <!-- 年 -->
              <div class="mb-3">
                <label class="form-label fw-bold">
                  <i class="fas fa-calendar-alt me-1"></i>年
                </label>
                <select class="form-select" v-model.number="selectedYear">
                  <option v-for="y in 5" :key="y" :value="2021 + y">{{ 2021 + y }}年</option>
                </select>
              </div>

              <!-- 月 -->
              <div class="mb-3">
                <label class="form-label fw-bold">
                  <i class="fas fa-calendar me-1"></i>月
                </label>
                <select class="form-select" v-model.number="selectedMonth">
                  <option v-for="m in 12" :key="m" :value="m">{{ m }}月</option>
                </select>
              </div>

              <!-- 日 -->
              <div class="mb-3">
                <label class="form-label fw-bold">
                  <i class="fas fa-calendar-day me-1"></i>日
                </label>
                <select class="form-select" v-model.number="selectedDay">
                  <option :value="null">指定なし</option>
                  <option v-for="d in 31" :key="d" :value="d">{{ d }}日</option>
                </select>
              </div>

              <!-- 曜日 -->
              <div class="mb-3">
                <label class="form-label fw-bold">
                  <i class="fas fa-calendar-week me-1"></i>曜日
                </label>
                <select class="form-select" v-model.number="selectedWeekday">
                  <option :value="null">指定なし</option>
                  <option v-for="(w,i) in ['日','月','火','水','木','金','土']" :key="i" :value="i">{{ w }}曜日</option>
                </select>
              </div>

              <!-- 検索ボタン -->
              <div class="d-grid gap-2">
                <button 
                  class="btn btn-primary btn-lg" 
                  @click="fetchClassPastRecords" 
                  :disabled="isLoading"
                >
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-search me-2"></i>
                  {{ isLoading ? '検索中...' : '検索' }}
                </button>
              </div>

              <!-- 条件リセット -->
              <div class="d-grid gap-2 mt-2">
                <button class="btn btn-outline-secondary btn-sm" @click="resetFilters">
                  <i class="fas fa-redo me-2"></i>条件リセット
                </button>
              </div>

            </div>
          </div>
        </div>

        <!-- 右側メインコンテンツ -->
        <div class="col-12 col-md-9">
          <div class="card">

            <div class="card-body">

              <!-- ローディング -->
              <div v-if="isLoading" class="text-center my-5">
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                  <span class="visually-hidden">読み込み中...</span>
                </div>
                <p class="mt-3 text-muted">データを取得中...</p>
              </div>

              <!-- メッセージ -->
              <div v-if="message && !isLoading" class="alert" :class="records.length ? 'alert-info' : 'alert-warning'">
                <i class="fas fa-info-circle me-2"></i>{{ message }}
              </div>

              <!-- 結果が0件の場合 -->
              <div v-if="!records.length && !isLoading && !message" class="text-center text-muted my-5">
                <i class="fas fa-search fa-3x mb-3"></i>
                <p>左の検索条件を設定して「検索」ボタンを押してください</p>
              </div>

              <!-- 結果テーブル -->
              <div v-if="records.length && !isLoading">

                <div class="table-responsive">
                  <table class="table table-bordered table-hover">
                    <thead class="table-light">
                      <tr>
                        <th style="width: 100px;" class="text-center">詳細</th>
                        <th style="width: 120px;">生徒名</th>
                        <th style="width: 80px;" class="text-center">体調</th>
                        <th style="width: 80px;" class="text-center">メンタル</th>
                        <th style="width: 140px;">提出日</th>
                        <th style="width: 100px;" class="text-center">確認状態</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="record in paginatedRecords" :key="record.student_id + record.student_name">
                        <td class="text-center">
                          <button class="btn btn-sm btn-outline-primary" @click="showDetail(record)">
                            <i class="fas fa-eye me-1"></i>確認
                          </button>
                        </td>
                        <td 
                          :class="{
                            'text-danger fw-bold': record.physical_condition <= 2 || record.mental_state <= 2
                          }"
                          style="white-space: nowrap;"
                        >
                          <i 
                            v-if="record.physical_condition <= 2 || record.mental_state <= 2" 
                            class="fas fa-exclamation-triangle me-1"
                          ></i>
                          {{ record.student_name }}
                        </td>
                        <td class="text-center">
                          <span class="badge" :class="{
                            'bg-danger': record.physical_condition <= 2,
                            'bg-warning text-dark': record.physical_condition === 3,
                            'bg-success': record.physical_condition >= 4
                          }">
                            {{ record.physical_condition }}
                          </span>
                        </td>
                        <td class="text-center">
                          <span class="badge" :class="{
                            'bg-danger': record.mental_state <= 2,
                            'bg-warning text-dark': record.mental_state === 3,
                            'bg-success': record.mental_state >= 4
                          }">
                            {{ record.mental_state }}
                          </span>
                        </td>
                        <td>{{ formatDate(record.created_at) }}</td>
                        <td class="text-center">
                          <span v-if="record.teacher_checked" class="badge bg-success">
                            <i class="fas fa-check me-1"></i>既読
                          </span>
                          <span v-else class="badge bg-warning text-dark">
                            <i class="fas fa-clock me-1"></i>未読
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <!-- ページネーション -->
                <nav class="d-flex justify-content-center my-3">
                  <ul class="pagination">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                      <button class="page-link" @click="changePage(currentPage - 1)">
                        <i class="fas fa-chevron-left me-1"></i>前へ
                      </button>
                    </li>
                    <li class="page-item disabled">
                      <span class="page-link">ページ {{ currentPage }} / {{ totalPages }}</span>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                      <button class="page-link" @click="changePage(currentPage + 1)">
                        次へ<i class="fas fa-chevron-right ms-1"></i>
                      </button>
                    </li>
                  </ul>
                </nav>
              </div>

            </div>
          </div>
        </div>

      </div>

      <!-- 詳細表示モーダル -->
      <div v-if="showModal" class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5);">
        <div class="modal-dialog modal-dialog-centered modal-lg">
          <div class="modal-content">
            <div class="modal-header bg-primary text-white">
              <h5 class="modal-title">
                <i class="fas fa-file-alt me-2"></i>連絡帳詳細
              </h5>
              <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
            </div>
            <div class="modal-body" v-if="selectedRecord">
              <div class="row g-3">
                
                <!-- 生徒名 -->
                <div class="col-md-8">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        <i class="fas fa-user me-1"></i>生徒名
                      </h6>
                      <p class="card-text fs-5">{{ selectedRecord.student_name }}</p>
                    </div>
                  </div>
                </div>

                <!-- 確認状態 -->
                <div class="col-md-4">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        <i class="fas fa-check-circle me-1"></i>確認状態
                      </h6>
                      <p class="card-text">
                        <span v-if="selectedRecord.teacher_checked" class="badge bg-success fs-6">
                          <i class="fas fa-check me-1"></i>既読
                        </span>
                        <span v-else class="badge bg-warning text-dark fs-6">
                          <i class="fas fa-clock me-1"></i>未読
                        </span>
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 体調 -->
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        <i class="fas fa-heartbeat me-1"></i>体調
                      </h6>
                      <p class="card-text">
                        <span class="badge fs-5" :class="{
                          'bg-danger': selectedRecord.physical_condition <= 2,
                          'bg-warning text-dark': selectedRecord.physical_condition === 3,
                          'bg-success': selectedRecord.physical_condition >= 4
                        }">
                          {{ selectedRecord.physical_condition || '-' }}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>

                <!-- メンタル -->
                <div class="col-md-6">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        <i class="fas fa-brain me-1"></i>メンタル
                      </h6>
                      <p class="card-text">
                        <span class="badge fs-5" :class="{
                          'bg-danger': selectedRecord.mental_state <= 2,
                          'bg-warning text-dark': selectedRecord.mental_state === 3,
                          'bg-success': selectedRecord.mental_state >= 4
                        }">
                          {{ selectedRecord.mental_state || '-' }}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 体調・メンタルメモ -->
                <div class="col-12">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        <i class="fas fa-notes-medical me-1"></i>体調・メンタル備考
                      </h6>
                      <div class="border rounded p-3 bg-light">
                        {{ selectedRecord.physical_mental_notes || '記載なし' }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 今日の振り返り -->
                <div class="col-12">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        <i class="fas fa-pencil-alt me-1"></i>今日の振り返り
                      </h6>
                      <div class="border rounded p-3 bg-light">
                        {{ selectedRecord.daily_reflection || '記載なし' }}
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 提出日 -->
                <div class="col-12">
                  <div class="card">
                    <div class="card-body">
                      <h6 class="card-subtitle mb-2 text-muted">
                        <i class="fas fa-clock me-1"></i>提出日時
                      </h6>
                      <p class="card-text">{{ formatDateFull(selectedRecord.created_at) }}</p>
                    </div>
                  </div>
                </div>

              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">
                <i class="fas fa-times me-2"></i>閉じる
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
};
