// アカウント情報の変更
const AccountModification = {
  emits: ['back-to-management'],
  components: {
    'search-accounts': SearchAccounts // SearchAccounts.js を読み込んでおく
  },
  data() {
    return {
      selectedUser: null, // 選択されたユーザー情報
      searchResults: [], // 検索結果を格納
      editForm: {
        user_id: '',
        username: '',
        admission_year: '',
        graduation_year: '',
        email: '',
        affiliation: '',
        role: ''
      },
      schools: ['A校', 'B校', 'C校', 'D校', 'E校'], // 所属校の選択肢
      roles: ['ユーザー', '図書委員', '司書', '管理者'], // 権限の選択肢
      isEditing: false, // 編集モード判定
      isLoading: false,
      error: '',
      successMessage: ''
    };
  },
  methods: {
    handleSearchCompleted(results) {
      // SearchAccounts.js から検索結果が返ってきたらここで受け取る
      this.searchResults = results;
      this.clearMessages();
    },
    selectUserForEdit(user) {
      // ユーザーを編集用に選択
      this.selectedUser = { ...user };
      this.editForm = { ...user };
      this.isEditing = true;
      this.clearMessages();
    },
    cancelEdit() {
      // 編集をキャンセル
      this.selectedUser = null;
      this.editForm = {
        user_id: '',
        username: '',
        admission_year: '',
        graduation_year: '',
        email: '',
        affiliation: '',
        role: ''
      };
      this.isEditing = false;
      this.clearMessages();
    },
    async saveChanges() {
      try {
        this.isLoading = true;
        this.error = '';
        this.successMessage = '';

        // バリデーション
        if (!this.editForm.username.trim()) {
          throw new Error('ユーザー名は必須です。');
        }
        if (!this.editForm.email.trim()) {
          throw new Error('メールアドレスは必須です。');
        }

        // API呼び出し（実装例）
        const payload = {
          user_id: this.editForm.user_id,
          updates: {
            username: this.editForm.username.trim(),
            admission_year: parseInt(this.editForm.admission_year),
            graduation_year: parseInt(this.editForm.graduation_year),
            email: this.editForm.email.trim(),
            affiliation: this.editForm.affiliation.trim(),
            role: this.editForm.role
          }
        };

        const response = await axios.post('http://127.0.0.1:8000/account-management/update-account', payload);
        
        // 成功時の処理
        this.successMessage = 'アカウント情報を更新しました。';
        
        // 検索結果も更新
        const index = this.searchResults.findIndex(u => u.user_id === this.editForm.user_id);
        if (index !== -1) {
          this.searchResults[index] = { ...this.editForm };
        }
        
        // 2秒後に検索画面に戻る
        setTimeout(() => {
          this.cancelEdit();
        }, 2000);

      } catch (err) {
        this.error = 'アカウント情報の更新中にエラーが発生しました：' + (err.response?.data?.detail || err.message);
      } finally {
        this.isLoading = false;
      }
    },
    clearMessages() {
      this.error = '';
      this.successMessage = '';
    }
  },
  template: `
    <div>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>アカウント情報変更</h2>
        <button @click="$emit('back-to-management')" class="btn btn-secondary">戻る</button>
      </div>

      <!-- 編集中でない場合は検索機能を表示 -->
      <div v-if="!isEditing">
        <!-- 検索コンポーネント -->
        <search-accounts 
          @search-completed="handleSearchCompleted">
        </search-accounts>

        <!-- 検索結果表示 -->
        <div v-if="searchResults.length > 0" class="mt-4">
          <h5>検索結果（{{ searchResults.length }}件）- 変更するアカウントを選択してください</h5>
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
                  <th>操作</th>
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
                  <td>
                    <span class="badge" :class="{
                      'bg-danger': user.role === '管理者',
                      'bg-warning': user.role === '司書', 
                      'bg-success': user.role === '図書委員',
                      'bg-info': user.role === 'ユーザー'
                    }">
                      {{ user.role }}
                    </span>
                  </td>
                  <td>
                    <button @click="selectUserForEdit(user)" class="btn btn-warning btn-sm">
                      <i class="bi bi-pencil me-1"></i>変更
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 編集フォーム -->
      <div v-if="isEditing" class="mt-4">
        <div class="card">
          <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">{{ selectedUser.username }} さんの情報を編集</h5>
            <button @click="cancelEdit()" class="btn btn-sm btn-outline-secondary">
              <i class="bi bi-x me-1"></i>編集をキャンセル
            </button>
          </div>
          <div class="card-body">
            <!-- 成功メッセージ -->
            <div v-if="successMessage" class="alert alert-success">
              <i class="bi bi-check-circle me-2"></i>{{ successMessage }}
            </div>
            
            <!-- エラーメッセージ -->
            <div v-if="error" class="alert alert-danger">
              <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
            </div>

            <form @submit.prevent="saveChanges()">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">ユーザーID（変更不可）</label>
                  <input type="text" class="form-control bg-light" v-model="editForm.user_id" readonly>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">ユーザー名 <span class="text-danger">*</span></label>
                  <input type="text" class="form-control" v-model="editForm.username" required>
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">入学年</label>
                  <input type="number" class="form-control" v-model="editForm.admission_year">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">卒業予定年</label>
                  <input type="number" class="form-control" v-model="editForm.graduation_year">
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">メールアドレス <span class="text-danger">*</span></label>
                  <input type="email" class="form-control" v-model="editForm.email" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">所属校</label>
                  <select class="form-select" v-model="editForm.affiliation">
                    <option value="">所属校を選択してください</option>
                    <option v-for="school in schools" :key="school" :value="school">{{ school }}</option>
                  </select>
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">権限</label>
                  <select class="form-select" v-model="editForm.role">
                    <option value="">権限を選択してください</option>
                    <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
                  </select>
                </div>
              </div>
              
              <div class="d-flex gap-2">
                <button type="submit" class="btn btn-success" :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-check me-1"></i>
                  変更を保存
                </button>
                <button type="button" @click="cancelEdit()" class="btn btn-outline-secondary">
                  <i class="bi bi-x me-1"></i>キャンセル
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  `
};
