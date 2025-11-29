<template>
    <div class="d-flex justify-content-center mt-4 px-2">
      <div class="w-100" style="max-width: 1200px;">
        
        <!-- ヘッダー部分 -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="mb-0">
            <i class="fas fa-search me-2"></i>検索結果
            <span class="badge bg-primary ms-2">{{ results.length }}件</span>
            <small v-if="results.length > perPage" class="text-muted ms-2">
              ({{ (currentPage - 1) * perPage + 1 }}～{{ Math.min(currentPage * perPage, results.length) }}件目を表示)
            </small>
          </h5>
          
          <!-- ナビゲーションボタン -->
          <div class="d-flex gap-2">
            <button class="btn btn-outline-secondary btn-sm" @click="$emit('back-to-search')">
              <i class="fas fa-arrow-left me-1"></i>検索画面に戻る
            </button>
            <button class="btn btn-outline-secondary btn-sm" @click="$emit('back-to-menu')">
              <i class="fas fa-home me-1"></i>メニューに戻る
            </button>
          </div>
        </div>

        <!-- 検索結果がない場合 -->
        <div v-if="results.length === 0" class="alert alert-info text-center">
          <i class="fas fa-info-circle me-2"></i>
          検索結果がありません
        </div>

        <!-- 検索結果テーブル -->
        <div v-else class="card">
          <div class="table-responsive">
            <table class="table table-bordered table-hover mb-0">
              <thead class="table-light">
                <tr class="text-center">
                  <th v-for="col in displayColumns" :key="col.key" :style="{ width: col.width }">
                    {{ col.label }}
                  </th>
                  <th style="width: 100px;">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in paginatedResults" :key="item.id">
                  <td v-for="col in displayColumns" :key="col.key" 
                      :class="col.key === 'fullName' ? '' : 'text-center'">
                    <span v-if="col.isStatus" class="badge" :class="getStatusClass(item[col.key])">
                      {{ getStatusLabel(item[col.key]) }}
                    </span>
                    <span v-else>{{ getCellValue(item, col) }}</span>
                  </td>
                  <td class="text-center">
                    <button class="btn btn-sm btn-primary"
                            @click="$emit('select-account', item)">
                      <i class="fas fa-edit me-1"></i>編集
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- ページネーション -->
          <div v-if="totalPages > 1" class="card-footer bg-white">
            <nav class="d-flex justify-content-center">
              <ul class="pagination mb-0">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <button class="page-link" @click="changePage(currentPage - 1)">
                    <i class="fas fa-chevron-left"></i> 前へ
                  </button>
                </li>
                <li class="page-item disabled">
                  <span class="page-link">
                    ページ {{ currentPage }} / {{ totalPages }}
                  </span>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <button class="page-link" @click="changePage(currentPage + 1)">
                    次へ <i class="fas fa-chevron-right"></i>
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>

      </div>
    </div>
</template>

<script>
export default {
  props: {
    results: {
      type: Array,
      default: () => [],
    },
  },
  emits: ["select-account", "back-to-search", "back-to-menu"],
  data() {
    return {
      currentPage: 1,
      perPage: 10
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.results.length / this.perPage) || 1;
    },
    paginatedResults() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.results.slice(start, end);
    },
    // ✅ 役割に応じた表示列を動的に決定
    displayColumns() {
      if (this.results.length === 0) return [];
      
      // 結果の最初の項目の役割を確認（複数役割が混在する場合は全項目表示）
      const roles = [...new Set(this.results.map(r => r.role))];
      
      if (roles.length === 1) {
        const role = roles[0];
        
        if (role === '教師') {
          return [
            { key: 'id', label: 'ID', width: '60px' },
            { key: 'fullName', label: '氏名', width: '120px' },
            { key: 'role', label: '役割', width: '80px' },
            { key: 'teacher_role', label: '教員区分', width: '110px' },
            { key: 'subject', label: '担当科目', width: '120px' },
            { key: 'grade', label: '学年', width: '70px', suffix: '年' },
            { key: 'className', label: 'クラス', width: '70px', suffix: '組' },
            { key: 'enrollmentYear', label: '登録年', width: '90px', suffix: '年' },
            { key: 'status', label: '状態', width: '90px', isStatus: true }
          ];
        } else if (role === '生徒') {
          return [
            { key: 'id', label: 'ID', width: '60px' },
            { key: 'fullName', label: '氏名', width: '120px' },
            { key: 'grade', label: '学年', width: '80px', suffix: '年' },
            { key: 'className', label: 'クラス', width: '80px', suffix: '組' },
            { key: 'status', label: '状態', width: '100px', isStatus: true }
          ];
        } else if (role === '養護教諭') {
          return [
            { key: 'id', label: 'ID', width: '80px' },
            { key: 'fullName', label: '氏名', width: '120px' },
            { key: 'role', label: '役割', width: '120px' },
            { key: 'status', label: '状態', width: '100px', isStatus: true }
          ];
        } else if (role === '管理者') {
          return [
            { key: 'id', label: 'ID', width: '60px' },
            { key: 'fullName', label: '氏名', width: '120px' },
            { key: 'role', label: '役割', width: '80px' },
            { key: 'grade', label: '学年', width: '70px', suffix: '年' },
            { key: 'className', label: 'クラス', width: '70px', suffix: '組' },
            { key: 'status', label: '状態', width: '90px', isStatus: true }
          ];
        }
      }
      
      // 複数役割が混在する場合は全項目表示
      return [
        { key: 'id', label: 'ID', width: '60px' },
        { key: 'fullName', label: '氏名', width: '120px' },
        { key: 'role', label: '役割', width: '80px' },
        { key: 'teacher_role', label: '教員区分', width: '110px' },
        { key: 'subject', label: '担当科目', width: '120px' },
        { key: 'grade', label: '学年', width: '70px', suffix: '年' },
        { key: 'className', label: 'クラス', width: '70px', suffix: '組' },
        { key: 'enrollmentYear', label: '登録年', width: '90px', suffix: '年' },
        { key: 'status', label: '状態', width: '90px', isStatus: true }
      ];
    }
  },
  methods: {
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    getStatusLabel(status) {
      const statusMap = {
        'enrolled': '在籍',
        'graduated': '卒業',
        'transferred': '転校',
        'suspended': '休学',
        'on_leave': '休学',
        'other': 'その他'
      };
      return statusMap[status] || status;
    },
    getStatusClass(status) {
      const classMap = {
        'enrolled': 'bg-success',
        'graduated': 'bg-secondary',
        'transferred': 'bg-warning',
        'suspended': 'bg-danger',
        'on_leave': 'bg-danger',
        'other': 'bg-info'
      };
      return classMap[status] || 'bg-secondary';
    },
    getCellValue(item, column) {
      const value = item[column.key];
      
      if (value === null || value === undefined || value === '' || value === 0) {
        return '-';
      }
      
      return value + (column.suffix || '');
    }
  },
  watch: {
    results() {
      this.currentPage = 1;
    }
  }
};
</script>
