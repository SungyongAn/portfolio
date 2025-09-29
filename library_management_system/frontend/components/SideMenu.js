
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
                    <div v-else class="menu-item d-flex flex-column align-items-start p-2 text-decoration-none rounded bg-success text-white">
                        <div>{{ currentUser.username }}</div>
                        <div class="small">{{ currentUser.affiliation }}</div>
                        <button @click="$emit('logout')" class="btn btn-sm btn-outline-light align-self-end mt-2">ログアウト</button>
                    </div>
                </li>

                <!-- 管理者権限でのみ表示されるメニュー -->
                <li v-if="isLoggedIn && currentUser && currentUser.role === '管理者'" class="mb-2">
                    <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                        :class="{ 'bg-primary text-white': currentPage === 'user-management', 'text-dark': currentPage !== 'user-management' }"
                        @click="$emit('page-change', 'user-management')"
                        style="cursor: pointer;">
                        ユーザー管理
                    </div>
                    <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                        :class="{ 'bg-primary text-white': currentPage === 'material-management', 'text-dark': currentPage !== 'material-management' }"
                        @click="$emit('page-change', 'material-management')"
                        style="cursor: pointer;">
                        資料管理
                    </div>
                </li>
            </ul>
        </div>
    `
};
