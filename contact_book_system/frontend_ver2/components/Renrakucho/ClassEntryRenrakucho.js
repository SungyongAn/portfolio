// 教師用 生徒の連絡帳提出状況の確認、更新用の親コンポーネント
const ClassEntryRenrakucho = {
  components: {
    ClassRenrakuchoSearch,
    RenrakuchoList
  },
  props: ['currentUser'],
  emits: ['back', 'updateTitle'],
  data() {
    return {
      records: []
    };
  },
  mounted() {
    // ヘッダーにタイトルと戻るボタンを設定
    this.$emit('updateTitle', {
      title: '未確認の連絡帳',
      icon: 'fas fa-calendar-day',
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
    handleSearchResult(data) {
      this.records = data;
    },
    async reloadAfterUpdate() {
      this.$refs.searchComp.fetchUnviewedRecords();
    },
    backToMenu() {
      this.$emit('back');
    }
  },
  template: `
    <div class="card p-4">

      <!-- 検索部分 -->
      <ClassRenrakuchoSearch
        ref="searchComp"
        :currentUser="currentUser"
        @searchResult="handleSearchResult"
      />

      <!-- 結果一覧部分 -->
      <RenrakuchoList
        v-if="records.length"
        :records="records"
        @update="reloadAfterUpdate"
      />

    </div>
  `
};
