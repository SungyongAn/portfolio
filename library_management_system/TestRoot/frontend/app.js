Vue.createApp({
    data() {
        return {
            appName: '図書館システム',
            version: '1.0.0',
            currentUser: null,
            isLoggedIn: false,
            currentPage: 'top' // 'top', 'login', 'search', 'manage', 'user'
        };
    },

components: {
    TopPage,
    SideMenu,
    LoginPage
},

methods: {
    setUser(user) {
        this.currentUser = user;
        this.isLoggedIn = true;
    },
    logout() {
        this.currentUser = null;
        this.isLoggedIn = false;
        this.currentPage = 'top';
    },
    navigateTo(page) {
        this.currentPage = page;
    },
    handleLoginSuccess(userData) {
        this.setUser(userData);
        this.currentPage = 'top';
        alert(`ようこそ、${userData.userId}さん！`);
    },
    handleMenuClick(page) {
        if (page === 'logout') {
            if (confirm('ログアウトしますか?')) {
                this.logout();
            }
        } else {
            this.navigateTo(page);
        }
    }
}
}).mount("#app");
