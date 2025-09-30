const MaterialRegistrationStep1 = {
    emits: ['barcode-checked'],
    data() {
        return {
            barcode: '',
            isLoading: false,
            errorMessage: ''
        };
    },
    methods: {
        async checkBarcode() {
            this.isLoading = true;
            this.errorMessage = '';

            try {
                const response = await axios.post(
                    'http://127.0.0.1:8000/material-management/check_barcode',
                    { barcode: this.barcode }
                );

                if (response.data.exists) {
                    this.errorMessage = 'このバーコードは既に登録されています。';
                } else {
                    // 親へイベント発火 → Step2へ遷移
                    this.$emit('barcode-checked', this.barcode);
                }
            } catch (error) {
                this.errorMessage = 'バーコード確認でエラーが発生しました。';
            } finally {
                this.isLoading = false;
            }
        }
    },
    template: `
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">バーコード入力</h5>
            </div>
            <div class="card-body">
                <div class="mb-3">
                    <label class="form-label">バーコード番号</label>
                    <input type="text" class="form-control" v-model="barcode">
                </div>

                <div v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</div>

                <button class="btn btn-primary" @click="checkBarcode" :disabled="isLoading || !barcode.trim()">
                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                    確認
                </button>
            </div>
        </div>
    `
};
