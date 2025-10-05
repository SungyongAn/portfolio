const MaterialRegistrationStep2 = {
    props: ['barcode'],
    emits: ['back-to-step1', 'material-registered'],
    data() {
        return {
            materialForm: {
                barcode: this.barcode,
                title: '',
                author: '',
                publisher: '',
                ndc_code: '999',
                type_name: '図書',
                affiliation: 'A校',
                shelf: ''
            },
            ndcOptions: [
                { value: '999', label: '未登録' },
                { value: '000', label: '哲学' },
                { value: '100', label: '歴史' },
                { value: '200', label: '社会科学' },
                { value: '300', label: '自然科学' },
                { value: '400', label: '技術・工学' },
                { value: '500', label: '産業' },
                { value: '600', label: '芸術' },
                { value: '700', label: '言語' },
                { value: '800', label: '文学' }
            ],
            typeOptions: ['図書', '雑誌', '新聞', '視聴覚資料', '電子資料'],
            affiliationOptions: ['A校', 'B校', 'C校', 'D校', 'E校'],
            isLoading: false,
            errorMessage: '',
            successMessage: '',
            registeredMaterial: null
        };
    },
    methods: {
        async registerMaterial() {
            if (!this.materialForm.title.trim() || !this.materialForm.author.trim()) {
                this.errorMessage = 'タイトルと著者は必須です。';
                return;
            }

            const confirmed = confirm(`以下の内容で登録します。よろしいですか？\n\nバーコード番号: ${this.materialForm.barcode}\nタイトル: ${this.materialForm.title}\n著者: ${this.materialForm.author}`);
            if (!confirmed) return;

            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';

            try {
                const response = await axios.post(
                    'http://127.0.0.1:8000/material-management/register',
                    this.materialForm
                );

                if (response.data.success) {
                    console.log('Response data:', response.data);
                    console.log('Material:', response.data.material);
                    // データを登録
                    this.registeredMaterial = response.data.material;

                    console.log('registeredMaterial set to:', this.registeredMaterial);
                    // DOM 更新を待ってからメッセージ表示
                    this.$nextTick(() => {
                      console.log('nextTick executed');
                      this.successMessage = '資料が正常に登録されました。';
                      this.$emit('material-registered', this.registeredMaterial);
                    });
                } else {
                    this.errorMessage = response.data.message || '登録に失敗しました。';
                }
            } catch (error) {
                console.error('Registration error:', error);
                if (error.response) {
                    this.errorMessage = error.response.data.detail || '資料の登録に失敗しました。';
                } else {
                    this.errorMessage = '資料の登録に失敗しました。サーバーに接続できません。';
                }
            } finally {
                this.isLoading = false;
            }
        },

        resetForm() {
            this.registeredMaterial = null;
            this.successMessage = '';
            this.errorMessage = '';
            this.$emit('back-to-step1');
        }
    },
    
    template: `
    <div class="card">
      <div class="card-header d-flex justify-content-between align-items-center">
        <h5 class="mb-0">詳細情報入力</h5>
        <button class="btn btn-outline-secondary btn-sm" @click="resetForm">← 別のバーコードを入力</button>
      </div>

      <div class="card-body">
        <!-- 登録成功後の表示 -->
        <template v-if="registeredMaterial">
          <div class="alert alert-success mb-3">
            <i class="bi bi-check-circle-fill me-2"></i>
            {{ successMessage }}
          </div>

          <h6 class="mb-3">登録済み資料情報</h6>
          <div class="table-responsive">
            <table class="table table-bordered">
              <tbody>
                <tr><th class="bg-light">資料ID</th><td>{{ registeredMaterial.material_id }}</td></tr>
                <tr><th class="bg-light">バーコード番号</th><td>{{ registeredMaterial.barcode }}</td></tr>
                <tr><th class="bg-light">タイトル</th><td>{{ registeredMaterial.title }}</td></tr>
                <tr><th class="bg-light">著者名</th><td>{{ registeredMaterial.author }}</td></tr>
                <tr><th class="bg-light">出版社</th><td>{{ registeredMaterial.publisher || '未指定' }}</td></tr>
                <tr><th class="bg-light">分類(NDC)</th><td>{{ registeredMaterial.ndc_code }}</td></tr>
                <tr><th class="bg-light">種別</th><td>{{ registeredMaterial.type_name }}</td></tr>
                <tr><th class="bg-light">学校名</th><td>{{ registeredMaterial.affiliation }}</td></tr>
                <tr><th class="bg-light">棚版</th><td>{{ registeredMaterial.shelf || '未指定' }}</td></tr>
                <tr><th class="bg-light">登録日</th><td>{{ registeredMaterial.registration_date }}</td></tr>
              </tbody>
            </table>
          </div>

          <div class="d-flex justify-content-center mt-4">
            <button class="btn btn-primary btn-lg" @click="resetForm">
              <i class="bi bi-plus-circle me-2"></i>新しい資料を登録
            </button>
          </div>
        </template>

        <!-- 入力フォーム -->
        <template v-else>
          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">バーコード番号</label>
              <input type="text" class="form-control bg-light" v-model="materialForm.barcode" readonly disabled>
            </div>
            <div class="col-md-6">
              <label class="form-label">書籍タイトル <span class="text-danger">*</span></label>
              <input type="text" class="form-control" v-model="materialForm.title" required>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">著者名 <span class="text-danger">*</span></label>
              <input type="text" class="form-control" v-model="materialForm.author" required>
            </div>
            <div class="col-md-6">
              <label class="form-label">出版社</label>
              <input type="text" class="form-control" v-model="materialForm.publisher">
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">分類(NDC) <span class="text-danger">*</span></label>
              <select class="form-select" v-model="materialForm.ndc_code" required>
                <option v-for="option in ndcOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">種別 <span class="text-danger">*</span></label>
              <select class="form-select" v-model="materialForm.type_name" required>
                <option v-for="type in typeOptions" :key="type" :value="type">{{ type }}</option>
              </select>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <label class="form-label">学校名 <span class="text-danger">*</span></label>
              <select class="form-select" v-model="materialForm.affiliation" required>
                <option v-for="school in affiliationOptions" :key="school" :value="school">{{ school }}</option>
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">棚版</label>
              <input type="text" class="form-control" v-model="materialForm.shelf">
            </div>
          </div>

          <div v-if="errorMessage" class="alert alert-danger">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ errorMessage }}
          </div>
          
          <div v-if="successMessage" class="alert alert-success">
            <i class="bi bi-check-circle-fill me-2"></i> {{ successMessage }}
          </div>

          <div class="d-flex justify-content-end gap-2">
            <button class="btn btn-secondary" @click="resetForm">キャンセル</button>
            <button class="btn btn-primary" @click="registerMaterial" :disabled="isLoading">
              <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span> 登録
            </button>
          </div>
        </template>
      </div>
    </div>
  `
};
