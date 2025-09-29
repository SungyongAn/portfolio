const MaterialRegistration = {
    props: [],
    emits: ['back-to-material-management'],
    data() {
        return {
            // 現在のステップ（'barcode' | 'details'）
            currentStep: 'barcode',
            
            barcodeForm: {
                barcode: ''
            },
            materialForm: {
                title: '',
                author: '',
                publisher: '',
                isbn: '',
                publicationYear: '',
                category: '一般書',
                location: ''
            },
            
            isScanning: false,
            isLoading: false,
            errorMessage: '',
            successMessage: '',
            barcodeCheckResult: null
        };
    },
    methods: {
        // バーコードを手動で入力
        handleBarcodeInput() {
            if (this.barcodeForm.barcode.trim()) {
                this.checkBarcodeExists(this.barcodeForm.barcode.trim());
            }
        },

        // バーコードスキャン開始（将来的な拡張用）
        startBarcodeScanning() {
            this.isScanning = true;
            this.errorMessage = '';
            // 実際のバーコードスキャン機能はここに実装
            // 現在はダミーとして2秒後にサンプルバーコードを生成
            setTimeout(() => {
                const dummyBarcode = '9784' + Math.floor(Math.random() * 100000000).toString().padStart(8, '0');
                this.barcodeForm.barcode = dummyBarcode;
                this.isScanning = false;
                this.checkBarcodeExists(dummyBarcode);
            }, 2000);
        },

        // バーコードスキャン停止
        stopBarcodeScanning() {
            this.isScanning = false;
        },

        // バーコードの重複確認
        async checkBarcodeExists(barcode) {
            this.isLoading = true;
            this.errorMessage = '';
            this.barcodeCheckResult = null;

            try {
                // 実際のAPI呼び出し
                const response = await axios.post('http://127.0.0.1:8000/material-management/check_barcode', {
                    barcode: barcode
                });

                if (response.data.exists) {
                    this.barcodeCheckResult = { exists: false, barcode: barcode, message: data.message };
                    this.successMessage = data.message;  // 受け取ったメッセージをそのまま表示
                    this.materialForm.isbn = barcode;
                    this.currentStep = 'details';
                } else {
                    this.barcodeCheckResult = { exists: true, barcode: barcode };
                    
                    this.successMessage = 'バーコードの確認が完了しました。詳細情報を入力してください。';
                    // ISBNをフォームにセット
                    this.materialForm.isbn = barcode;
                    // 詳細入力ステップに進む
                    this.currentStep = 'details';
                }
            } catch (error) {
                console.error('バーコード確認エラー:', error);
                if (error.response && error.response.data && error.response.data.detail) {
                    this.errorMessage = `エラー: ${error.response.data.detail}`;
                } else if (error.response && error.response.status === 404) {
                    this.errorMessage = 'APIエンドポイントが見つかりません。サーバーが起動していることを確認してください。';
                } else if (error.code === 'ECONNREFUSED' || error.message.includes('Network Error')) {
                    this.errorMessage = 'サーバーに接続できません。サーバーが起動していることを確認してください。';
                } else {
                    this.errorMessage = 'バーコードの確認中にエラーが発生しました。';
                }
            } finally {
                this.isLoading = false;
            }
        },

        // 別のバーコードを入力（バーコード入力に戻る）
        inputAnotherBarcode() {
            this.currentStep = 'barcode';
            this.barcodeForm.barcode = '';
            this.materialForm = {
                title: '',
                author: '',
                publisher: '',
                isbn: '',
                publicationYear: '',
                category: '一般書',
                location: ''
            };
            this.errorMessage = '';
            this.successMessage = '';
            this.barcodeCheckResult = null;
        },

        // 外部APIから資料情報を自動取得（オプション）
        async fetchMaterialInfo() {
            if (!this.materialForm.isbn) return;

            this.isLoading = true;
            try {
                // 実際のAPI呼び出し（Google Books API、国立国会図書館API等）
                // 現在はダミーデータ
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // ダミーの資料情報で自動入力
                this.materialForm.title = 'サンプル書籍タイトル - ' + this.materialForm.isbn;
                this.materialForm.author = '山田太郎';
                this.materialForm.publisher = 'サンプル出版社';
                this.materialForm.publicationYear = '2023';
                
                this.successMessage = '資料情報を自動取得しました。必要に応じて修正してください。';
            } catch (error) {
                this.errorMessage = '資料情報の自動取得に失敗しました。手動で入力してください。';
            } finally {
                this.isLoading = false;
            }
        },

        // 資料を登録
        async registerMaterial() {
            // 必須項目チェック
            if (!this.materialForm.title.trim() || !this.materialForm.author.trim()) {
                this.errorMessage = 'タイトルと著者は必須項目です。';
                return;
            }

            this.isLoading = true;
            this.errorMessage = '';
            this.successMessage = '';

            try {
                // 実際のAPI呼び出しをここに実装
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                this.successMessage = '資料が正常に登録されました。';
                
                // フォームを完全にリセット
                this.resetForm();
                
            } catch (error) {
                this.errorMessage = '資料の登録に失敗しました。';
            } finally {
                this.isLoading = false;
            }
        },

        // フォーム全体をリセット
        resetForm() {
            this.currentStep = 'barcode';
            this.barcodeForm.barcode = '';
            this.materialForm = {
                title: '',
                author: '',
                publisher: '',
                isbn: '',
                publicationYear: '',
                category: '一般書',
                location: ''
            };
            this.errorMessage = '';
            this.successMessage = '';
            this.barcodeCheckResult = null;
        }
    },
    template: `
        <div class="container-fluid">
            <div class="row">
                <div class="col-12">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h2>資料の追加</h2>
                        <button @click="$emit('back-to-material-management')" class="btn btn-secondary">
                            資料管理に戻る
                        </button>
                    </div>


                    <!-- バーコード入力・確認 -->
                    <div v-if="currentStep === 'barcode'" class="card">
                        <div class="card-header">
                            <h5 class="card-title mb-0">バーコード確認</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-8">
                                    <div class="mb-3">
                                        <label for="barcode" class="form-label">バーコード（ISBN等）</label>
                                        <div class="input-group">
                                            <input 
                                                type="text" 
                                                class="form-control" 
                                                id="barcode"
                                                v-model="barcodeForm.barcode"
                                                placeholder="バーコードを入力またはスキャンしてください"
                                                @keyup.enter="handleBarcodeInput"
                                                :disabled="isScanning || isLoading">
                                            <button 
                                                class="btn btn-primary" 
                                                type="button"
                                                @click="handleBarcodeInput"
                                                :disabled="!barcodeForm.barcode.trim() || isScanning || isLoading">
                                                重複確認
                                            </button>
                                        </div>
                                        <div class="form-text">
                                            まず重複がないかを確認します。確認後、詳細情報の入力に進みます。
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label">バーコードスキャン</label>
                                    <div class="d-grid gap-2">
                                        <button 
                                            v-if="!isScanning"
                                            class="btn btn-success" 
                                            @click="startBarcodeScanning"
                                            :disabled="isLoading">
                                            📷 スキャン開始
                                        </button>
                                        <button 
                                            v-else
                                            class="btn btn-warning" 
                                            @click="stopBarcodeScanning">
                                            ⏹ スキャン停止
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- スキャン中の表示 -->
                            <div v-if="isScanning" class="alert alert-info mt-3">
                                <div class="d-flex align-items-center">
                                    <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                                    バーコードをスキャンしています...
                                </div>
                            </div>

                            <!-- ローディング表示 -->
                            <div v-if="isLoading && !isScanning" class="alert alert-info mt-3">
                                <div class="d-flex align-items-center">
                                    <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                                    バーコードの重複を確認しています...
                                </div>
                            </div>

                            <!-- エラーメッセージ -->
                            <div v-if="errorMessage" class="alert alert-danger mt-3">
                                {{ errorMessage }}
                            </div>

                            <!-- 成功メッセージ -->
                            <div v-if="successMessage && currentStep === 'barcode'" class="alert alert-success mt-3">
                                {{ successMessage }}
                            </div>
                        </div>
                    </div>

                    <!-- ステップ2: 詳細情報入力 -->
                    <div v-if="currentStep === 'details'" class="card">
                        <div class="card-header d-flex justify-content-between align-items-center">
                            <h5 class="card-title mb-0">ステップ2: 詳細情報入力</h5>
                            <button class="btn btn-outline-secondary btn-sm" @click="inputAnotherBarcode">
                                ← 別のバーコードを入力
                            </button>
                        </div>
                        <div class="card-body">
                            <!-- 確認済みバーコード表示 -->
                            <div class="alert alert-success mb-3">
                                <strong>確認済みバーコード:</strong> {{ materialForm.isbn }}
                            </div>

                            <!-- 自動取得ボタン -->
                            <div class="mb-3">
                                <button class="btn btn-info" @click="fetchMaterialInfo" :disabled="isLoading">
                                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                                    📚 資料情報を自動取得
                                </button>
                                <small class="text-muted ms-2">外部データベースから資料情報を取得します（オプション）</small>
                            </div>

                            <div class="row">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">タイトル <span class="text-danger">*</span></label>
                                        <input type="text" class="form-control" v-model="materialForm.title" 
                                               placeholder="書籍のタイトルを入力" required>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">著者 <span class="text-danger">*</span></label>
                                        <input type="text" class="form-control" v-model="materialForm.author" 
                                               placeholder="著者名を入力" required>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">出版社</label>
                                        <input type="text" class="form-control" v-model="materialForm.publisher" 
                                               placeholder="出版社名を入力">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label class="form-label">ISBN</label>
                                        <input type="text" class="form-control" v-model="materialForm.isbn" readonly>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">出版年</label>
                                        <input type="text" class="form-control" v-model="materialForm.publicationYear" 
                                               placeholder="例: 2023">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">分類</label>
                                        <select class="form-select" v-model="materialForm.category">
                                            <option value="一般書">一般書</option>
                                            <option value="参考書">参考書</option>
                                            <option value="雑誌">雑誌</option>
                                            <option value="新聞">新聞</option>
                                            <option value="DVD">DVD</option>
                                            <option value="その他">その他</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">配置場所</label>
                                <input type="text" class="form-control" v-model="materialForm.location" 
                                       placeholder="例: A棟2階、文学コーナー">
                            </div>

                            <!-- エラーメッセージ -->
                            <div v-if="errorMessage" class="alert alert-danger">
                                {{ errorMessage }}
                            </div>

                            <!-- 成功メッセージ -->
                            <div v-if="successMessage && currentStep === 'details'" class="alert alert-success">
                                {{ successMessage }}
                            </div>
                            
                            <div class="d-flex justify-content-end gap-2">
                                <button class="btn btn-secondary" @click="resetForm">
                                    キャンセル
                                </button>
                                <button class="btn btn-primary" @click="registerMaterial" :disabled="isLoading">
                                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                                    資料を登録
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};
