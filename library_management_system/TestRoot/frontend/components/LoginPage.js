const LoginPage = {
    data() {
        return {
            userId: '',
            password: '',
            showPassword: false,
            errorMessage: '',
            isLoading: false
        };
    },
    methods: {
        async handleLogin() {
            // バリデーション
            if (!this.userId) {
                this.errorMessage = 'ユーザーIDを入力してください';
                return;
            }
            if (!this.password) {
                this.errorMessage = 'パスワードを入力してください';
                return;
            }

            this.isLoading = true;
            this.errorMessage = '';

            try {
                // ApiClientを使用してバックエンドにログインリクエストを送信
                const result = await ApiClient.login(this.userId, this.password);
                
                if (result.success) {
                    console.log('ログイン成功:', result.data);
                    
                    // 親コンポーネントにログイン成功を通知
                    this.$emit('login-success', {
                        userId: this.userId,
                        timestamp: new Date(),
                        message: result.message
                    });
                    
                    // フォームをリセット
                    this.resetForm();
                } else {
                    // ログイン失敗
                    this.errorMessage = result.message || 'ログインに失敗しました';
                }
                
            } catch (error) {
                this.errorMessage = 'ログインに失敗しました。もう一度お試しください。';
                console.error('ログインエラー:', error);
            } finally {
                this.isLoading = false;
            }
        },
        resetForm() {
            this.userId = '';
            this.password = '';
            this.showPassword = false;
            this.errorMessage = '';
        },
        togglePasswordVisibility() {
            this.showPassword = !this.showPassword;
        },
        handleCancel() {
            this.resetForm();
            this.$emit('cancel');
        }
    },
    template: `
        <div class="container-fluid bg-light min-vh-100 d-flex align-items-center justify-content-center">
            <div class="card shadow-lg" style="max-width: 450px; width: 100%;">
                <div class="card-header bg-primary text-white text-center py-3">
                    <h3 class="mb-0">
                        <i class="bi bi-person-circle me-2"></i>ログイン
                    </h3>
                </div>
                <div class="card-body p-4">
                    <!-- エラーメッセージ -->
                    <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i>
                        {{ errorMessage }}
                        <button type="button" class="btn-close" @click="errorMessage = ''" aria-label="Close"></button>
                    </div>

                    <form @submit.prevent="handleLogin">
                        <!-- ユーザーID入力 -->
                        <div class="mb-3">
                            <label for="userId" class="form-label fw-bold">
                                <i class="bi bi-person me-2"></i>ユーザーID
                            </label>
                            <input 
                                type="text" 
                                class="form-control form-control-lg" 
                                id="userId"
                                v-model="userId"
                                placeholder="ユーザーIDを入力"
                                :disabled="isLoading"
                                autocomplete="username"
                            >
                        </div>

                        <!-- パスワード入力 -->
                        <div class="mb-4">
                            <label for="password" class="form-label fw-bold">
                                <i class="bi bi-lock me-2"></i>パスワード
                            </label>
                            <div class="input-group">
                                <input 
                                    :type="showPassword ? 'text' : 'password'" 
                                    class="form-control form-control-lg" 
                                    id="password"
                                    v-model="password"
                                    placeholder="パスワードを入力"
                                    :disabled="isLoading"
                                    autocomplete="current-password"
                                >
                                <button 
                                    class="btn btn-outline-secondary" 
                                    type="button"
                                    @click="togglePasswordVisibility"
                                    :disabled="isLoading"
                                >
                                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                                </button>
                            </div>
                        </div>

                        <!-- ボタン -->
                        <div class="d-grid gap-2">
                            <button 
                                type="submit" 
                                class="btn btn-primary btn-lg"
                                :disabled="isLoading"
                            >
                                <span v-if="isLoading">
                                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                    ログイン中...
                                </span>
                                <span v-else>
                                    <i class="bi bi-box-arrow-in-right me-2"></i>ログイン
                                </span>
                            </button>
                            <button 
                                type="button" 
                                class="btn btn-outline-secondary"
                                @click="handleCancel"
                                :disabled="isLoading"
                            >
                                <i class="bi bi-x-circle me-2"></i>キャンセル
                            </button>
                        </div>
                    </form>

                    <!-- パスワードを忘れた場合のリンク -->
                    <div class="text-center mt-3">
                        <a href="#" class="text-decoration-none small">
                            <i class="bi bi-question-circle me-1"></i>パスワードを忘れた場合
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `
};
