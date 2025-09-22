
const SideMenu = {
    props: ['currentPage', 'isLoggedIn', 'currentUser'],
    emits: ['page-change', 'logout'],
    template: `
        <div class="flex-shrink-0 p-3 bg-light border-end" style="width: 280px;">
            <div class="d-flex align-items-center pb-3 mb-3 border-bottom">
                メニュー
            </div>
            
            <ul class="list-unstyled">
                <li class="mb-2">
                    <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                        :class="{ 'bg-primary text-white': currentPage === 'top', 'text-dark': currentPage !== 'top' }"
                        @click="$emit('page-change', 'top')"
                        style="cursor: pointer;">
                        TOPページ
                    </div>
                </li>
                <li class="mb-2">
                    <div v-if="!isLoggedIn" 
                        class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                        :class="{ 'bg-primary text-white': currentPage === 'login', 'text-dark': currentPage !== 'login' }"
                        @click="$emit('page-change', 'login')"
                        style="cursor: pointer;">
                        ログイン
                    </div>
                    <div v-else class="menu-item d-flex align-items-center justify-content-between p-2 text-decoration-none rounded bg-success text-white">
                        <span>{{ currentUser.username }}</span>
                        <button @click="$emit('logout')" class="btn btn-sm btn-outline-light">ログアウト</button>
                    </div>
                </li>
            </ul>
        </div>
    `
};
