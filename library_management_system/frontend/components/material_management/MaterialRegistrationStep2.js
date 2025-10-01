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
                ndc_code: '未登録',
                type_name: '図書',
                affiliation: 'A校',
                shelf: ''
            },
            ndcOptions: [
                { value: '未登録', label: '未登録' },
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

            const confirmed = confirm(`以下の内容で登録します。よろしいですか？\n\nバーコード番号: ${this.materialForm.barcode}\nタイトル: ${this.materialForm.title}\n著者: ${this.materialForm.author}\n出版社: ${this.materialForm.publisher}\n分類(NDC): ${this.materialForm.ndc_code}\n種別: ${this.materialForm.type_name}\n学校名: ${this.materialForm.affiliation}\n棚版: ${this.materialForm.shelf || '未指定'}`);
            
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
                    this.registeredMaterial = response.data.material;
                    this.successMessage = '資料が正常に登録されました。';
                    this.$emit('material-registered', this.registeredMaterial);
                } else {
                    this.errorMessage = response.data.message || '登録に失敗しました。';
                }
            } catch (error) {
                console.error('Registration error:', error);
                this.errorMessage = '資料の登録に失敗しました。';
            } finally {
                this.isLoading = false;
            }
        }
    },
    template: `
    <div class="card">
        <div class="card-header d-flex justify-content-between align-items-center">
            <h5 class="mb-0">詳細情報入力</h5>
            <button class="btn btn-outline-secondary btn-sm" @click="$emit('back-to-step1')">
                ← 別のバーコードを入力
            </button>
        </div>

        <div class="card-body">
            <div v-if="registeredMaterial">
                <h6>登録済み資料情報</h6>
                <ul class="list-group mb-3">
                    <li class="list-group-item"><strong>バーコード:</strong> {{ registeredMaterial.barcode }}</li>
                    <li class="list-group-item"><strong>タイトル:</strong> {{ registeredMaterial.title }}</li>
                    <li class="list-group-item"><strong>著者:</strong> {{ registeredMaterial.author }}</li>
                    <li class="list-group-item"><strong>出版社:</strong> {{ registeredMaterial.publisher }}</li>
                    <li class="list-group-item"><strong>NDC:</strong> {{ registeredMaterial.ndc_code }}</li>
                    <li class="list-group-item"><strong>種別:</strong> {{ registeredMaterial.type_name }}</li>
                    <li class="list-group-item"><strong>学校名:</strong> {{ registeredMaterial.affiliation }}</li>
                    <li class="list-group-item"><strong>棚版:</strong> {{ registeredMaterial.shelf || '未指定' }}</li>
                    <li class="list-group-item"><strong>登録日:</strong> {{ registeredMaterial.registration_date }}</li>
                </ul>
                <button class="btn btn-primary" @click="$emit('back-to-step1')">新しい資料を登録</button>
            </div>

            <div v-else>
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
                            <option v-for="type in typeOptions" :key="type" :value="type">
                                {{ type }}
                            </option>
                        </select>
                    </div>
                </div>

                <div class="row mb-3">
                    <div class="col-md-6">
                        <label class="form-label">学校名 <span class="text-danger">*</span></label>
                        <select class="form-select" v-model="materialForm.affiliation" required>
                            <option v-for="school in affiliationOptions" :key="school" :value="school">
                                {{ school }}
                            </option>
                        </select>
                    </div>
                    <div class="col-md-6">
                        <label class="form-label">棚版</label>
                        <input type="text" class="form-control" v-model="materialForm.shelf">
                    </div>
                </div>

                <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>
                <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>

                <div class="d-flex justify-content-end gap-2">
                    <button class="btn btn-secondary" @click="$emit('back-to-step1')">キャンセル</button>
                    <button class="btn btn-primary" @click="registerMaterial" :disabled="isLoading">
                        <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                        登録
                    </button>
                </div>
            </div>
        </div>
    </div>
    `
};
