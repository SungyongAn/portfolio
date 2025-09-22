
const SetPasswordForm = {
    props: ['passwordForm', 'verifiedUser', 'showNewPassword', 'showConfirmPassword'],
    emits: ['set-password', 'toggle-new-password', 'toggle-confirm-password', 'page-change'],
    template: `
        <div class="set-password-container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h2 class="card-title text-center mb-4">パスワードの登録</h2>
                            
                            <div class="alert alert-info text-center mb-4">
                                <strong>{{ verifiedUser.username }}</strong> さんのパスワードを設定してください
                            </div>

                            <form @submit.prevent="$emit('set-password')">
                                <div class="mb-3">
                                    <label for="newPassword" class="form-label">新しいパスワード</label>
                                    <input 
                                        :type="showNewPassword ? 'text' : 'password'" 
                                        id="newPassword" 
                                        v-model="passwordForm.password" 
                                        class="form-control"
                                        placeholder="パスワードを入力"
                                        minlength="8"
                                        required>
                                </div>

                                <div class="mb-3">
                                    <label for="confirmPassword" class="form-label">パスワード（確認用）</label>
                                    <input 
                                        :type="showConfirmPassword ? 'text' : 'password'" 
                                        id="confirmPassword" 
                                        v-model="passwordForm.confirmPassword" 
                                        class="form-control"
                                        placeholder="パスワードを再入力"
                                        minlength="8"
                                        required>
                                    <div v-if="passwordForm.password && passwordForm.confirmPassword && passwordForm.password !== passwordForm.confirmPassword" 
                                        class="form-text text-danger">
                                        パスワードが一致しません
                                    </div>
                                </div>

                                <div class="form-check mb-2">
                                    <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        id="showNewPassword" 
                                        :checked="showNewPassword"
                                        @change="$emit('toggle-new-password')">
                                    <label class="form-check-label" for="showNewPassword">
                                        新しいパスワードを表示
                                    </label>
                                </div>
                                <div class="form-check mb-3">
                                    <input 
                                        class="form-check-input" 
                                        type="checkbox" 
                                        id="showConfirmPassword" 
                                        :checked="showConfirmPassword"
                                        @change="$emit('toggle-confirm-password')">
                                    <label class="form-check-label" for="showConfirmPassword">
                                        確認用パスワードを表示
                                    </label>
                                </div>

                                <div class="alert alert-secondary small mb-3">
                                    <strong>パスワード要件：</strong>
                                    <ul class="mb-0 mt-1">
                                        <li>8文字以上</li>
                                        <li>英数字を含む</li>
                                    </ul>
                                </div>

                                <button 
                                    type="submit" 
                                    class="btn btn-success w-100"
                                    :disabled="passwordForm.password !== passwordForm.confirmPassword || !passwordForm.password || passwordForm.password.length < 8">
                                    パスワードを登録
                                </button>
                                <button type="button" class="btn btn-link mt-2 w-100" @click="$emit('page-change', 'login')">
                                    ← ログイン画面へ戻る
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};
