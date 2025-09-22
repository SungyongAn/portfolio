Vue.createApp({
    data() {
        return {
            currentPage: 'top', // 最初の画面はTOP
            // ログイン画面の入力情報管理
            loginForm: {
                userId: '',
                password: ''
            },
            // ユーザー認証の情報管理
            firstAuthForm: { userId: '', email: '', emailConfirm: '' },
            // パスワード入力画面の情報管理
            passwordForm: { password: '', confirmPassword: '' },
            verifiedUser: null, // 初回ログイン時のパス設定前の認証済みユーザー名
            isLoading: false, // ログイン状態のフラグ
            loginError: '',
            loginSuccess: '',
            showPassword: false, // ログイン時のパスワード入力内容の表示フラグ
            showNewPassword: false, // 新しいパスワード表示フラグ
            showConfirmPassword: false, // 確認用パスワード表示フラグ
            currentUser: null, 
            isLoggedIn: false, // ログイン状態の管理
        };
    },

components: {
    SideMenu,
    TopPage,
    LoginForm,
    FirstAuthForm,
    SetPasswordForm
    },

methods: {
    // ページ切り替え時にログイン画面をリセット
    setCurrentPage(page) {
        if (page === 'login') {
            this.resetLoginForm();
        }
        if (page === 'firstAuth') {
            this.firstAuthForm = { userId: '', email: '', emailConfirm: '' };
        }
        if (page === 'setPassword') {
            this.passwordForm = { password: '', confirmPassword: '' };
            this.showNewPassword = false;
            this.showConfirmPassword = false;
        }
        this.currentPage = page;
    },

    // ログイン画面のリセット
    resetLoginForm() {
        this.loginForm.userId = '';
        this.loginForm.password = '';
        this.loginError = '';
        this.loginSuccess = '';
        this.showPassword = false;
        this.isLoading = false;
    },

    // ログアウト処理
    logout() {
        this.currentUser = null;
        this.isLoggedIn = false;
        this.currentPage = 'top';
        this.resetLoginForm();
    },

    // ログイン処理
    async handleLogin() {
        this.isLoading = true;
        this.loginError = '';
        this.loginSuccess = '';

        try {
            const response = await fetch("http://127.0.0.1:8000/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    userId: this.loginForm.userId,
                    password: this.loginForm.password
                })
            });

            if (!response.ok) {
                // HTTPエラーの場合、レスポンスボディからエラーメッセージを取得
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTPエラー: ${response.status}`);
            }

            const result = await response.json();
            
            // APIレスポンス形式: {"authority": "管理者"}
            if (result.authority) {
                this.currentUser = {
                    userId: this.loginForm.userId,
                    username: result.username,
                    role: result.authority
                };
                this.isLoggedIn = true;
                
                // フォームをクリア
                this.loginForm.userId = '';
                this.loginForm.password = '';
            } else {
                this.loginError = "予期しないレスポンス形式です";
            }
        } catch (error) {
            this.loginError = error.message || "サーバー通信エラーが発生しました";
        } finally {
            this.isLoading = false;
        }
    },

    // パスワード設定処理
    async handleFirstAuth() {
        // メールアドレスの一致確認
        if (this.firstAuthForm.email !== this.firstAuthForm.emailConfirm) {
            alert('メールアドレスが一致しません');
            return;
        }

        // 必須項目チェック
        if (!this.firstAuthForm.userId || !this.firstAuthForm.email) {
            alert('すべての項目を入力してください');
            return;
        }

        try {
            // APIへの送信処理
            const response = await fetch("http://127.0.0.1:8000/auth/first-auth", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    userId: this.firstAuthForm.userId,
                    email: this.firstAuthForm.email
                })
                
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTPエラー: ${response.status}`);
            }

            const result = await response.json();

            if (result.success) {
                // ユーザー情報を保存して、パスワード入力画面に遷移
                this.verifiedUser = {
                    userId: this.firstAuthForm.userId,
                    username: result.username
                };
                // パスワード入力画面に遷移
                this.setCurrentPage('setPassword');
            } else {
                alert(result.message || 'ユーザー情報の認証に失敗しました');
            }
        } catch (error) {
            console.error('パスワード設定エラー:', error);
            alert('エラーが発生しました: ' + error.message);
        }
    },

    // パスワード登録処理
    async handleSetPassword() {
        // パスワードの一致確認
        if (this.passwordForm.password !== this.passwordForm.confirmPassword) {
            alert('パスワードが一致しません');
            return;
        }

        // パスワード長チェック
        if (this.passwordForm.password.length < 8) {
            alert('パスワードは8文字以上で入力してください');
            return;
        }

        try {
            // APIへの送信処理
            const response = await fetch("http://127.0.0.1:8000/auth/set-password", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    userId: this.verifiedUser.userId,
                    password: this.passwordForm.password
                })
            });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || `HTTPエラー: ${response.status}`);
                }

                const result = await response.json();

                if (result.success) {
                    alert('パスワードの登録が完了しました。ログイン画面からログインしてください。');
                    // 全てのフォームをクリア
                    this.firstAuthForm = { userId: '', email: '', emailConfirm: '' };
                    this.passwordForm = { password: '', confirmPassword: '' };
                    this.verifiedUser = null;
                    // ログイン画面に戻る
                    this.setCurrentPage('login');
                } else {
                    alert(result.message || 'パスワードの登録に失敗しました');
                }
            } catch (error) {
                console.error('パスワード登録エラー:', error);
                alert('エラーが発生しました: ' + error.message);
            }
    },
}
}).mount("#app")
