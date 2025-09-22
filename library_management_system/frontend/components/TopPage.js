const TopPage = {
    props: ['isLoggedIn', 'currentUser'],
    template: `
        <div>
            <h1 class="fs-2 fw-bold text-center mb-0">図書館へようこそ</h1>
            <div v-if="isLoggedIn" class="text-center mt-4">
                <p class="text-muted">{{ currentUser.username }}さん、こんにちは！</p>
            </div>
        </div>
    `
};
