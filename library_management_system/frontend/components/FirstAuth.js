// パスワード設定認証コンポーネント
const FirstAuthForm = {
    props: ['firstAuthForm'],
    emits: ['first-auth', 'page-change'],
    template: `
        <div class="first-auth-container">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-body">
                            <h2 class="card-title text-center mb-4">ユーザー情報の認証</h2>
                            <form @submit.prevent="$emit('first-auth')">
                                <div class="mb-3">
                                    <label for="firstAuthId" class="form-label">ユーザーID</label>
                                    <input 
                                        type="text" 
                                        id="firstAuthUserId" 
                                        v-model="firstAuthForm.userId" 
                                        class="form-control" 
                                        required>
                                </div>

                                <div class="mb-3">
                                    <label for="firstAuthEmail" class="form-label">メールアドレス</label>
                                    <input 
                                        type="email" 
                                        id="firstAuthEmail" 
                                        v-model="firstAuthForm.email" 
                                        class="form-control" 
                                        required>
                                </div>

                                <div class="mb-3">
                                    <label for="firstAuthEmailConfirm" class="form-label">メールアドレス（確認用）</label>
                                    <input 
                                        type="email" 
                                        id="firstAuthEmailConfirm" 
                                        v-model="firstAuthForm.emailConfirm" 
                                        class="form-control" 
                                        required>
                                </div>

                                <button 
                                    type="submit" 
                                    class="btn btn-warning w-100"
                                    :disabled="firstAuthForm.email !== firstAuthForm.emailConfirm || !firstAuthForm.email">
                                    ユーザー情報の認証
                                </button>
                                <button class="btn btn-link mt-2 w-100" @click="$emit('page-change', 'login')">
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
