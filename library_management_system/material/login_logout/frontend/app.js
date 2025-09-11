const app = Vue.createApp({
    data() {
        return {
            currentView: 'home', // 'login' or 'first-login'
            loginForm: { userId: '', password: '' },
            firstLoginForm: { userId: '', email: '' },
        };
    },
    methods: {
        showLoginForm() {
            this.currentView = 'login';
        },
        showFirstLoginForm() {
            this.currentView = 'first-login';
        },
        async login() {
            const response = await fetch("http://127.0.0.1:8000/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(this.loginForm)
            });
            const result = await response.json();
            alert(result.message || "ログイン成功");
        },
        // async passwordReset() {

        // },
        async firstLogin() {
            const response = await fetch("http://127.0.0.1:8000/auth/first-login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(this.firstLoginForm)
            });
            const result = await response.json();
            alert(result.message || "登録しました");
        },
        logout() {
            this.currentView = 'home';
            this.loginForm = { userId: '', password: '' };
            this.firstLoginForm = { userId: '', email: '' };
            alert("ログアウトしました");
        }
    }
});

app.mount("#app");
