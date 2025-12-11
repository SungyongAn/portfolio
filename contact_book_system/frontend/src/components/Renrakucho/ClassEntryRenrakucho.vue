<template>
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
</template>

<script>
import ClassRenrakuchoSearch from "./ClassRenrakuchoSearch.vue";
import RenrakuchoList from "./RenrakuchoList.vue";

export default {
  name: "ClassEntryRenrakucho",
  components: {
    ClassRenrakuchoSearch,
    RenrakuchoList,
  },

  props: ["currentUser"],
  emits: ["updateTitle"], // ★ back は不要になった

  data() {
    return {
      records: [],
    };
  },

  mounted() {
    // ヘッダーにタイトルと戻るボタンを設定
    this.$emit("updateTitle", {
      title: "未確認の連絡帳",
      icon: "fas fa-calendar-day",
      showBackButton: true,
      onBack: this.backToMenu, // ★ Router の戻る動作を渡す
    });
  },

  beforeUnmount() {
    // コンポーネント離脱時にタイトルをクリア
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false,
    });
  },

  methods: {
    handleSearchResult(data) {
      this.records = data;
    },

    async reloadAfterUpdate() {
      if (this.$refs.searchComp?.fetchUnviewedRecords) {
        await this.$refs.searchComp.fetchUnviewedRecords();
      }
    },

    /**
     * Vue Router で戻る
     */
    backToMenu() {
      this.$router.back(); // ★ Vue Router の戻る機能でページ遷移
    },
  },
};
</script>
