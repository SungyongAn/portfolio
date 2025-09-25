const UserManagement = {
    props: ['currentPage'],
    emits: ['page-change'],
    template: `
        <div class="container-fluid">
            <div class="row">
                <div class="col-12">
                    <h2 class="mb-4">ユーザー管理</h2>
                    
                    <ul class="list-unstyled">
                        <li class="mb-2">
                            <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                                :class="{ 'bg-primary text-white': currentPage === 'account-registration', 'text-dark': currentPage !== 'account-registration' }"
                                @click="$emit('page-change', 'account-registration')"
                                style="cursor: pointer;">
                                1. 新規アカウント登録
                            </div>
                        </li>

                        <li class="mb-2">
                            <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                                :class="{ 'bg-primary text-white': currentPage === 'account-deletion', 'text-dark': currentPage !== 'account-deletion' }"
                                @click="$emit('page-change', 'account-deletion')"
                                style="cursor: pointer;">
                                2. アカウントの削除
                            </div>
                        </li>

                        <li class="mb-2">
                            <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                                :class="{ 'bg-primary text-white': currentPage === 'account-modification', 'text-dark': currentPage !== 'account-modification' }"
                                @click="$emit('page-change', 'account-modification')"
                                style="cursor: pointer;">
                                3. アカウントの情報変更
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    `
};
