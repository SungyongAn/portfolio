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
            showPassword: false,  // ← 追加
        };
    },
methods: {
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
                this.loginSuccess = `ログイン成功！権限: ${result.authority}`;
                this.currentUser = {
                    userId: this.loginForm.userId,
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
