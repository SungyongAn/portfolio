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
  emits: ["updateTitle"],

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
    });
  },

  beforeUnmount() {
    // コンポーネント離脱時にタイトルをクリア
    this.$emit("updateTitle", {
      title: "",
      icon: "",
      showBackButton: false, // ← false に修正
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
  },
};
</script>
