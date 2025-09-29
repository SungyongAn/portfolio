const MaterialManagement = {
    props: ['currentPage'],
    emits: ['page-change'],
    template: `
        <div class="container-fluid">
            <div class="row">
                <div class="col-12">
                    <h2 class="mb-4">資料管理</h2>
                    
                    <ul class="list-unstyled">
                        <li class="mb-2">
                            <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                                :class="{ 'bg-primary text-white': currentPage === 'material-registration', 'text-dark': currentPage !== 'material-registration' }"
                                @click="$emit('page-change', 'material-registration')"
                                style="cursor: pointer;">
                                1. 資料の追加
                            </div>
                        </li>

                        <li class="mb-2">
                            <div class="menu-item d-flex align-items-center p-2 text-decoration-none rounded"
                                :class="{ 'bg-primary text-white': currentPage === 'material-deletion', 'text-dark': currentPage !== 'material-deletion' }"
                                @click="$emit('page-change', 'material-deletion')"
                                style="cursor: pointer;">
                                2. 資料の削除
                            </div>
                        </li>
                        
                    </ul>
                </div>
            </div>
        </div>
    `
};
