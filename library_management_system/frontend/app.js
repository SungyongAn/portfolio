Vue.createApp({
    data() {
        return {
            currentPage: 'top', // 最初の画面はTOP
            loginForm: {
                userId: '',
                password: ''
            },
            isLoading: false,
            loginError: '',
            loginSuccess: '',
            showPassword: false,
            currentUser: null, 
            isLoggedIn: false, // ログイン状態の管理
        };
    },

methods: {
    // ページ切り替え時にログイン画面をリセット
    setCurrentPage(page) {
        if (page === 'login') {
            this.resetLoginForm();
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

            console.log("実際のレスポンス:", result);
            console.log("success:", result.success);
            console.log("authority:", result.authority); 
            console.log("username:", result.username);
            
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
    }
}
}).mount("#app")
