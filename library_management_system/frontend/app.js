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
            loginSuccess: ''
        };
    },
    methods: {
        handleLogin() {
            this.isLoading = true;
            this.loginError = '';
            this.loginSuccess = '';

            // 疑似ログイン処理（実際はAPIと連携）
            setTimeout(() => {
                if (this.loginForm.userId === 'admin' && this.loginForm.password === '1234') {
                    this.loginSuccess = 'ログイン成功しました！';
                } else {
                    this.loginError = 'ユーザーIDまたはパスワードが間違っています。';
                }
                this.isLoading = false;
            }, 1000);
        }
    }
}).mount("#app")
