<template>
  <div class="d-flex justify-content-center">
    <div style="max-width: 700px">
      <div class="table-responsive">
        <table class="table table-bordered table-hover text-center mb-0">
          <thead class="table-light">
            <tr>
              <th>詳細</th>
              <th>日付</th>
              <th>生徒名</th>
              <th>提出日</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in paginatedRecords" :key="record.renrakucho_id">
              <td>
                <button class="btn btn-sm btn-info" @click="openModal(record)">
                  確認
                </button>
              </td>
              <td>{{ formatDate(record.record_date) }}</td>
              <td
                class="text-truncate"
                style="max-width: 8ch"
                :class="{ 'text-danger fw-bold': isCritical(record) }"
              >
                {{ record.student_name }}
              </td>
              <td>
                {{ formatDate(record.submitted_date || record.created_at) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- ページネーション -->
      <nav class="d-flex justify-content-center mt-3">
        <ul class="pagination mb-0">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <button class="page-link" @click="changePage(currentPage - 1)">
              前へ
            </button>
          </li>
          <li class="page-item disabled">
            <span class="page-link"
              >ページ {{ currentPage }} / {{ totalPages }}</span
            >
          </li>
          <li
            class="page-item"
            :class="{ disabled: currentPage === totalPages }"
          >
            <button class="page-link" @click="changePage(currentPage + 1)">
              次へ
            </button>
          </li>
        </ul>
      </nav>

      <!-- モーダル -->
      <div
        v-if="showModal"
        class="modal fade show d-block"
        style="background: rgba(0, 0, 0, 0.5)"
        tabindex="-1"
      >
        <div class="modal-dialog modal-dialog-centered">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">
                連絡帳詳細 - {{ selectedRecord.student_name }}
              </h5>
              <button
                type="button"
                class="btn-close"
                @click="closeModal"
              ></button>
            </div>
            <div class="modal-body text-center">
              <p>
                <strong>日付:</strong>
                {{ formatDate(selectedRecord.record_date) }}
              </p>

              <p>
                <strong>体調:</strong>
                <span
                  :class="{
                    'text-danger fw-bold':
                      selectedRecord.physical_condition <= 2,
                  }"
                >
                  {{ selectedRecord.physical_condition }}
                </span>
              </p>

              <p>
                <strong>メンタル:</strong>
                <span
                  :class="{
                    'text-danger fw-bold': selectedRecord.mental_state <= 2,
                  }"
                >
                  {{ selectedRecord.mental_state }}
                </span>
              </p>

              <p><strong>今日の振り返り:</strong></p>
              <p class="border p-2">{{ selectedRecord.daily_reflection }}</p>
            </div>

            <div class="modal-footer">
              <button class="btn btn-secondary" @click="closeModal">
                閉じる
              </button>
              <button
                class="btn btn-success"
                @click="markAsRead(selectedRecord)"
              >
                既読にする
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "RenrakuchoList",
  props: ["records"],
  emits: ["update"],
  data() {
    return {
      selectedRecord: null,
      showModal: false,
      currentPage: 1,
      perPage: 10,
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
  methods: {
    openModal(record) {
      this.selectedRecord = record;
      this.showModal = true;
    },
    closeModal() {
      this.selectedRecord = null;
      this.showModal = false;
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
    formatDate(dateStr) {
      if (!dateStr) return "-";
      const d = new Date(dateStr);
      return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
    },
    async markAsRead(record) {
      if (!record) return;
      const confirmed = confirm(
        `${record.student_name} さんの連絡帳を既読にしますか？`
      );
      if (!confirmed) return;

      try {
        const payload = { renrakucho_ids: [record.renrakucho_id] };
        const response = await axios.post(
          "http://127.0.0.1:8000/renrakucho-management/mark-as-read",
          payload
        );

        if (response.data.success) {
          alert(response.data.message || "既読更新が完了しました");
          this.$emit("update");
          this.closeModal();
        } else {
          alert(response.data.message || "既読更新に失敗しました");
        }
      } catch (error) {
        alert(error.response?.data?.detail || "サーバーとの通信に失敗しました");
      }
    },
    isCritical(record) {
      return record.physical_condition <= 2 || record.mental_state <= 2;
    },
  },
};
</script>

<style scoped>
.modal {
  z-index: 1050;
}
</style>
