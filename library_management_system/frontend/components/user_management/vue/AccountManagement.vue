<template>
  <div class="container-fluid">
    <h2 class="mb-4">ユーザー管理</h2>
    <!-- 検索コンポーネント -->
    <UserSearch @search-results="updateSearchResults" />

    <!-- 削除コンポーネント -->
    <UserDelete
      v-if="searchResults.length > 0"
      :search-results="searchResults"
      @delete-completed="onDeleteCompleted"
    />
  </div>
</template>

<script>
import UserSearch from "./UserSearch.vue";
import UserDelete from "./UserDelete.vue";

export default {
  components: { UserSearch, UserDelete },
  data() {
    return {
      searchResults: [],
    };
  },
  methods: {
    updateSearchResults(results) {
      this.searchResults = results;
    },
    onDeleteCompleted(updatedResults) {
      this.searchResults = updatedResults;
    },
  },
};
</script>
