const SearchAccounts = {
    emits: ['search-completed'],
    data() {
        return {
            searchCondition: { searchType: 'userId', searchValue: '' },
            searchOptions: [
                { value: 'userId', label: 'ユーザーID' },
                { value: 'username', label: 'ユーザー名' },
                { value: 'admission_year', label: '入学年' },
                { value: 'graduation_year', label: '卒業予定年' },
                { value: 'email', label: 'メールアドレス' },
                { value: 'affiliation', label: '所属校' }
            ],
            error: '',
            isLoading: false
        };
    },
    methods: {
        async handleSearch() {
            try {
                this.isLoading = true;
                this.error = '';

                const value = this.searchCondition.searchValue.toString().trim();
                if (!value) {
                    this.error = '検索条件を入力してください。';
                    return;
                }

                let filter = {};
                if (this.searchCondition.searchType === 'admission_year' || this.searchCondition.searchType === 'graduation_year') {
                    const num = parseInt(value);
                    if (isNaN(num)) throw new Error(`${this.searchCondition.searchType}は数値で入力してください。`);
                    filter[this.searchCondition.searchType] = num;
                } else {
                    filter[this.searchCondition.searchType] = value;
                }

                const payload = { filters: [filter] };
                const response = await axios.post('http://127.0.0.1:8000/account-management/search-accounts', payload);

                this.$emit('search-completed', response.data.users_list || []);
                if ((response.data.users_list || []).length === 0) this.error = '該当ユーザーが見つかりません';
            } catch (err) {
                this.error = '検索中にエラーが発生しました：' + (err.response?.data?.detail || err.message);
            } finally {
                this.isLoading = false;
            }
        },
        clearSearch() {
            this.searchCondition.searchType = 'userId';
            this.searchCondition.searchValue = '';
            this.error = '';
        },
        getInputType(searchType) {
            return (searchType === 'admission_year' || searchType === 'graduation_year') ? 'number' : 'text';
        },
        getInputPlaceholder(searchType) {
            const opt = this.searchOptions.find(o => o.value === searchType);
            return opt ? `${opt.label}を入力` : '';
        }
    },
    template: `
        <div class="card mb-3">
            <div class="card-body">
                <form @submit.prevent="handleSearch">
                    <div class="row mb-3">
                        <div class="col-md-3">
                            <label class="form-label">検索条件</label>
                            <select v-model="searchCondition.searchType" class="form-select">
                                <option v-for="opt in searchOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
                            </select>
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">検索値</label>
                            <input :type="getInputType(searchCondition.searchType)" class="form-control" 
                                v-model="searchCondition.searchValue" :placeholder="getInputPlaceholder(searchCondition.searchType)">
                        </div>
                    </div>
                    <button type="submit" class="btn btn-primary me-2" :disabled="isLoading">
                        検索
                        <span v-if="isLoading" class="spinner-border spinner-border-sm ms-2"></span>
                    </button>
                    <button type="button" class="btn btn-outline-secondary" @click="clearSearch">クリア</button>
                </form>
                <div v-if="error" class="alert alert-warning mt-2">{{ error }}</div>
            </div>
        </div>
    `
};
