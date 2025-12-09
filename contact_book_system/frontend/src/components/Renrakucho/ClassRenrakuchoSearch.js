// 教師の連絡帳検索
const ClassRenrakuchoSearch = {
  props: ['currentUser'],
  emits: ['searchResult'],
  data() {
    return {
      isLoading: false,
      message: ''
    };
  },
  methods: {
    async fetchUnviewedRecords() {
      if (!this.currentUser || this.currentUser.role !== 'teacher') {
        this.message = '教師のみ閲覧可能です';
        return;
      }

      this.isLoading = true;
      this.message = '';

      const payload = {
        grade: Number(this.currentUser.grade),
        class_name: this.currentUser.className
      };

      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/renrakucho-management/class-not-checked-renrakucho',
          payload
        );

        if (response.data.success) {
          const unviewed = response.data.data.filter(r => !r.teacher_checked);
          this.$emit('searchResult', unviewed);
          if (!unviewed.length) this.message = '本日の未閲覧の連絡帳はありません';
        } else {
          this.message = response.data.message || 'データ取得に失敗しました';
        }
      } catch (error) {
        if (error.response) {
          this.message = error.response.data.detail || 'データ取得に失敗しました';
        } else {
          this.message = 'サーバーとの通信に失敗しました';
        }
      } finally {
        this.isLoading = false;
      }
    }
  },
  mounted() {
    this.fetchUnviewedRecords();
  },
  template: `
    <div>
      <div v-if="isLoading" class="text-center my-3">
        <div class="spinner-border text-primary"></div>
      </div>

      <div v-if="message && !isLoading" class="alert alert-info">
        <i class="fas fa-info-circle me-2"></i>{{ message }}
      </div>
    </div>
  `
};
