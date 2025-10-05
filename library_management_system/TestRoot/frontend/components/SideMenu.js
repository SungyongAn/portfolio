const SideMenu = {
    data() {
        return {
            menuItems: [
                { id: 1, label: 'ログイン', icon: 'bi-box-arrow-in-right', page: 'login' },
                { id: 2, label: 'ログアウト', icon: 'bi-box-arrow-right', page: 'logout' },
                { id: 3, label: '資料の検索', icon: 'bi-search', page: 'search' },
                { id: 4, label: '資料管理', icon: 'bi-journal-text', page: 'manage' },
                { id: 5, label: 'ユーザー登録と削除', icon: 'bi-person-plus', page: 'user' }
            ]
        };
    },
    methods: {
        handleMenuClick(item) {
            console.log(`${item.label}が選択されました`);
            
            if (item.page === 'logout') {
                if (confirm('ログアウトしますか?')) {
                    this.$root.logout();
                }
            } else {
                this.$root.navigateTo(item.page);
            }
        }
    },
    template: `
        <div class="side-menu text-white">
            <div class="p-4 border-bottom border-secondary">
                <h2 class="h4 mb-0">
                    <i class="bi bi-list me-2"></i>メニュー
                </h2>
            </div>
            <div class="list-group list-group-flush">
                <a 
                    v-for="item in menuItems" 
                    :key="item.id"
                    href="#"
                    class="list-group-item list-group-item-action bg-dark text-white border-0 menu-item py-3"
                    @click.prevent="handleMenuClick(item)"
                >
                    <i :class="['bi', item.icon, 'me-3']"></i>
                    {{ item.label }}
                </a>
            </div>
        </div>
    `
};
