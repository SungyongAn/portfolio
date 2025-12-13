<template>
  <div class="container-fluid mt-4 px-2">
    <div class="row">
      <!-- 左サイドバー: 検索条件 -->
      <div class="col-12 col-md-3 mb-3">
        <div class="card h-100">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0"><i class="fas fa-filter me-2"></i>検索条件</h5>
          </div>
          <div class="card-body">
            <!-- 年 -->
            <div class="mb-3">
              <label class="form-label fw-bold"
                ><i class="fas fa-calendar-alt me-1"></i>年</label
              >
              <select class="form-select" v-model.number="selectedYear">
                <option v-for="y in 5" :key="y" :value="2021 + y">
                  {{ 2021 + y }}年
                </option>
              </select>
            </div>

            <!-- 月 -->
            <div class="mb-3">
              <label class="form-label fw-bold"
                ><i class="fas fa-calendar me-1"></i>月</label
              >
              <select class="form-select" v-model.number="selectedMonth">
                <option v-for="m in 12" :key="m" :value="m">{{ m }}月</option>
              </select>
            </div>

            <!-- 日 -->
            <div class="mb-3">
              <label class="form-label fw-bold"
                ><i class="fas fa-calendar-day me-1"></i>日</label
              >
              <select class="form-select" v-model.number="selectedDay">
                <option :value="null">指定なし</option>
                <option v-for="d in 31" :key="d" :value="d">{{ d }}日</option>
              </select>
            </div>

            <!-- 曜日 -->
            <div class="mb-3">
              <label class="form-label fw-bold"
                ><i class="fas fa-calendar-week me-1"></i>曜日</label
              >
              <select class="form-select" v-model.number="selectedWeekday">
                <option :value="null">指定なし</option>
                <option
                  v-for="(w, i) in ['日', '月', '火', '水', '木', '金', '土']"
                  :key="i"
                  :value="i"
                >
                  {{ w }}曜日
                </option>
              </select>
            </div>

            <!-- 検索ボタン -->
            <div class="d-grid gap-2">
              <button class="btn btn-primary btn-lg" @click="fetchRecords">
                <i class="fas fa-search me-2"></i>検索
              </button>
            </div>

            <!-- 条件リセット -->
            <div class="d-grid gap-2 mt-2">
              <button
                class="btn btn-outline-secondary btn-sm"
                @click="resetFilters"
              >
                <i class="fas fa-redo me-2"></i>日・曜日リセット
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
              <div
                class="spinner-border text-primary"
                style="width: 3rem; height: 3rem"
              ></div>
              <p class="mt-3 text-muted">データを取得中...</p>
            </div>

            <!-- メッセージ -->
            <div v-if="message && !isLoading" class="alert alert-info">
              <i class="fas fa-info-circle me-2"></i>{{ message }}
            </div>

            <!-- 結果テーブル -->
            <div v-if="records.length && !isLoading">
              <div class="alert alert-success mb-3">
                <i class="fas fa-check-circle me-2"></i>
                <strong>{{ records.length }}</strong
                >件の連絡帳が見つかりました
              </div>

              <div class="table-responsive">
                <table
                  class="table table-bordered table-hover"
                  style="table-layout: fixed"
                >
                  <thead class="table-light">
                    <tr>
                      <th style="width: 100px">詳細</th>
                      <th style="width: 200px">名前</th>
                      <th style="width: 120px">提出日</th>
                      <th style="width: 80px">体調</th>
                      <th style="width: 80px">メンタル</th>
                      <th style="width: 120px">担任の確認</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="record in paginatedRecords"
                      :key="record.record_date + record.id"
                    >
                      <td class="text-center">
                        <button
                          class="btn btn-sm btn-outline-primary"
                          @click="openModal(record)"
                        >
                          <i class="fas fa-eye me-1"></i>確認
                        </button>
                      </td>
                      <td
                        style="
                          white-space: nowrap;
                          overflow: hidden;
                          text-overflow: ellipsis;
                        "
                      >
                        {{ record.name || "-" }}
                      </td>
                      <td>
                        {{
                          formatDate(record.created_at || record.submitted_at)
                        }}
                      </td>
                      <td class="text-center">
                        <span
                          class="badge"
                          :class="{
                            'bg-danger': record.physical_condition <= 2,
                            'bg-warning': record.physical_condition === 3,
                            'bg-success': record.physical_condition >= 4,
                          }"
                        >
                          {{ record.physical_condition }}
                        </span>
                      </td>
                      <td class="text-center">
                        <span
                          class="badge"
                          :class="{
                            'bg-danger': record.mental_state <= 2,
                            'bg-warning': record.mental_state === 3,
                            'bg-success': record.mental_state >= 4,
                          }"
                        >
                          {{ record.mental_state }}
                        </span>
                      </td>
                      <td class="text-center">
                        <span
                          v-if="record.teacher_checked"
                          class="badge bg-success"
                        >
                          <i class="fas fa-check me-1"></i>確認済み
                        </span>
                        <span v-else class="badge bg-secondary">
                          <i class="fas fa-clock me-1"></i>未確認
                        </span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- ページネーション -->
              <nav
                class="d-flex justify-content-center my-3 align-items-center gap-2"
              >
                <!-- 最初ページ -->
                <button
                  class="btn btn-outline-primary btn-sm"
                  :disabled="currentPage === 1"
                  @click="changePage(1)"
                >
                  <i class="fas fa-angle-double-left me-1"></i>最初
                </button>

                <!-- 前ページ -->
                <button
                  class="btn btn-outline-primary btn-sm"
                  :disabled="currentPage === 1"
                  @click="changePage(currentPage - 1)"
                >
                  <i class="fas fa-chevron-left me-1"></i>前へ
                </button>

                <!-- ページジャンプ -->
                <div class="d-flex align-items-center gap-1">
                  <span>ページ:</span>
                  <input
                    type="number"
                    class="form-control"
                    v-model.number="jumpPage"
                    min="1"
                    :max="totalPages"
                    @keyup.enter="jumpToPage"
                    style="width: 80px"
                  />
                  <button
                    class="btn btn-outline-primary btn-sm"
                    @click="jumpToPage"
                  >
                    移動
                  </button>
                  <span>/ {{ totalPages }}</span>
                </div>

                <!-- 次ページ -->
                <button
                  class="btn btn-outline-primary btn-sm"
                  :disabled="currentPage === totalPages"
                  @click="changePage(currentPage + 1)"
                >
                  次へ<i class="fas fa-chevron-right ms-1"></i>
                </button>

                <!-- 最後ページ -->
                <button
                  class="btn btn-outline-primary btn-sm"
                  :disabled="currentPage === totalPages"
                  @click="changePage(totalPages)"
                >
                  最後<i class="fas fa-angle-double-right ms-1"></i>
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- モーダル -->
    <div
      v-if="showModal"
      class="modal fade show"
      tabindex="-1"
      style="display: block"
    >
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="fas fa-file-alt me-2"></i>連絡帳詳細
            </h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="closeModal"
            ></button>
          </div>
          <div class="modal-body">
            <pre>{{ selectedRecord }}</pre>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeModal">
              <i class="fas fa-times me-2"></i>閉じる
            </button>
          </div>
        </div>
      </div>
      <div class="modal-backdrop fade show" @click="closeModal"></div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import axios from "axios";

export default {
  name: "PastRenrakuchoSearch",
  props: ["currentUser"],
  data() {
    const today = new Date();
    return {
      selectedYear: today.getFullYear(),
      selectedMonth: today.getMonth() + 1,
      selectedDay: null,
      selectedWeekday: null,
      records: [],
      isLoading: false,
      message: "",
      currentPage: 1,
      perPage: 20,
      jumpPage: 1,
      selectedRecord: null,
      showModal: false,
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.records.length / this.perPage) || 1;
    },
    paginatedRecords() {
      const start = (this.currentPage - 1) * this.perPage;
      return this.records.slice(start, start + this.perPage);
    },
  },
  setup() {
    const router = useRouter();
    return { router };
  },
  mounted() {
    document.title = "過去の連絡帳検索";
    this.$emit("updateTitle", {
      title: "過去の連絡帳",
      icon: "fas fa-history",
      showBackButton: true,
      onBack: this.backToMenu,
    });
  },
  methods: {
    async fetchRecords() {
      if (!this.currentUser) return;

      this.isLoading = true;
      this.message = "";
      this.records = [];
      this.currentPage = 1;
      this.jumpPage = 1;

      const payload = {
        student_id: Number(this.currentUser.id),
        year: Number(this.selectedYear),
        month: Number(this.selectedMonth),
      };
      if (this.selectedDay) payload.day = Number(this.selectedDay);
      if (this.selectedWeekday !== null)
        payload.weekday = Number(this.selectedWeekday);

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/renrakucho-management/past-renrakucho-search",
          payload
        );
        this.records = response.data.data || [];
        if (!this.records.length)
          this.message = "該当する過去の連絡帳はありません";
      } catch (error) {
        console.error("取得エラー:", error);
        this.message = "過去の連絡帳の取得に失敗しました";
      } finally {
        this.isLoading = false;
      }
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      this.jumpPage = page;
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    jumpToPage() {
      if (this.jumpPage >= 1 && this.jumpPage <= this.totalPages) {
        this.changePage(this.jumpPage);
      } else {
        this.jumpPage = this.currentPage;
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return "-";
      const date = new Date(dateStr);
      const weekday = ["日", "月", "火", "水", "木", "金", "土"][date.getDay()];
      return `${date.getMonth() + 1}月${date.getDate()}日（${weekday}）`;
    },
    openModal(record) {
      this.selectedRecord = record;
      this.showModal = true;
    },
    closeModal() {
      this.selectedRecord = null;
      this.showModal = false;
    },
    resetFilters() {
      this.selectedDay = null;
      this.selectedWeekday = null;
    },
    goBack() {
      this.router.back();
    },
  },
};
</script>

<style scoped>
.modal-backdrop {
  z-index: 1040;
}
.modal {
  z-index: 1050;
}
</style>
