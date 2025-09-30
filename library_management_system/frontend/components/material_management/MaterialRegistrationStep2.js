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
                ndc: '999',
                type: '図書',
                school: 'A校',
                shelf: ''
            },
            isLoading: false,
            errorMessage: '',
            successMessage: ''
        };
    },
    methods: {
        async registerMaterial() {
            if (!this.materialForm.title.trim() || !this.materialForm.author.trim()) {
                this.errorMessage = 'タイトルと著者は必須です。';
                return;
            }

            const confirmed = confirm(`
                以下の内容で登録します。よろしいですか？
                バーコード番号: ${this.materialForm.barcode}
                タイトル: ${this.materialForm.title}
                著者: ${this.materialForm.author}
                出版社: ${this.materialForm.publisher}
                分類(NDC): ${this.materialForm.ndc}
                種別: ${this.materialForm.type}
                学校名: ${this.materialForm.school}
                棚版: ${this.materialForm.shelf || '未指定'}
            `);
            if (!confirmed) return;

            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';

            try {
                await axios.post(
                    'http://127.0.0.1:8000/material-management/register',
                    this.materialForm
                );
                this.successMessage = '資料が正常に登録されました。';
                this.$emit('material-registered');
            } catch (error) {
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
                <!-- 入力フォーム（タイトル、著者など） -->
                <div class="mb-3">
                    <label class="form-label">バーコード番号</label>
                    <input type="text" class="form-control" v-model="materialForm.barcode" readonly>
                </div>

                <div class="mb-3">
                    <label class="form-label">書籍タイトル *</label>
                    <input type="text" class="form-control" v-model="materialForm.title" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">著者名 *</label>
                    <input type="text" class="form-control" v-model="materialForm.author" required>
                </div>

                <!-- 省略: 出版社 / NDC / 種別 / 学校名 / 棚版 -->

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
    `
};
