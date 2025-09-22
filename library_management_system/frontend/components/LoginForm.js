const LoginForm = {
    props: ['loginForm', 'isLoading', 'loginError', 'loginSuccess', 'showPassword'],
    emits: ['login', 'toggle-password', 'page-change'],
    template: `
        <div class="login-container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h2 class="card-title text-center mb-4">ログイン</h2>

                            <div v-if="loginError" class="alert alert-danger">{{ loginError }}</div>
                            <div v-if="loginSuccess" class="alert alert-success">{{ loginSuccess }}</div>
                            
                            <form @submit.prevent="$emit('login')">
                                <div class="mb-3">
                                    <label for="userId" class="form-label">ユーザーID</label>
                                    <input 
                                        type="text" 
                                        id="userId"
                                        v-model="loginForm.userId"
                                        class="form-control"
                                        placeholder="ユーザーIDを入力"
                                        required
                                        :disabled="isLoading">
                                </div>
                                
                                <div class="mb-3">
                                    <label for="password" class="form-label">パスワード</label>
                                    <input 
                                        :type="showPassword ? 'text' : 'password'" 
                                        id="password"
                                        v-model="loginForm.password"
                                        class="form-control"
                                        placeholder="パスワードを入力"
                                        required
                                        :disabled="isLoading">
                                </div>
                                <div class="form-check mt-2">
                                    <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        id="showPassword" 
                                        :checked="showPassword"
                                        @change="$emit('toggle-password')">
                                    <label class="form-check-label" for="showPassword">
                                        パスワードを表示
                                    </label>
                                </div>
                                <button 
                                    type="submit" 
                                    class="btn btn-primary w-100"
                                    :disabled="isLoading || !loginForm.userId || !loginForm.password">
                                    ログイン
                                </button>
                            </form>
                            <div class="mt-3 d-grid gap-2">
                                <div class="mb-3">
                                    初めての方はこちら
                                    <button class="btn btn-outline-warning w-100" @click="$emit('page-change', 'firstAuth')">
                                        パスワードの設定
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};
