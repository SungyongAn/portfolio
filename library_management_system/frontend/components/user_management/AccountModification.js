const AccountModification = {
  emits: ['back-to-management'],
  components: {
    'search-accounts': SearchAccounts // SearchAccounts.js を読み込んでおく
  },
  data() {
    return {
      searchResults: [] // 検索結果を格納
    };
  },
  methods: {
    handleSearchCompleted(results) {
      // SearchAccounts.js から検索結果が返ってきたらここで受け取る
      this.searchResults = results;
    }
  },
  template: `
    <div>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>アカウント情報変更</h2>
        <button @click="$emit('back-to-management')" class="btn btn-secondary">戻る</button>
      </div>

      <!-- 検索コンポーネント -->
      <search-accounts 
        @search-completed="handleSearchCompleted">
      </search-accounts>

      <!-- 検索結果表示 -->
      <div v-if="searchResults.length > 0" class="mt-4">
        <h5>検索結果（{{ searchResults.length }}件）</h5>
        <div class="table-responsive">
          <table class="table table-striped table-hover">
            <thead class="table-dark">
              <tr>
                <th>ユーザーID</th>
                <th>ユーザー名</th>
                <th>入学年</th>
                <th>卒業予定年</th>
                <th>メールアドレス</th>
                <th>所属校</th>
                <th>権限</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in searchResults" :key="user.user_id">
                <td>{{ user.user_id }}</td>
                <td>{{ user.username }}</td>
                <td>{{ user.admission_year }}</td>
                <td>{{ user.graduation_year }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.affiliation }}</td>
                <td>{{ user.role }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `
};

