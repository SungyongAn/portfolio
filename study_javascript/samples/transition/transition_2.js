Vue.createApp({
    date: function() {
        return {
            isshow: false,
        }
    },
    methods: {
        beforeEnter: function(el) {
            // 要素が出現、表示する前の状態をここで定義
        },
        enter: function(el, done) {
            // elに出現、表示されるアニメーションを実行
            // アニメーションの終了後に done コールバックを呼び出す
        },
        afterEnter: function(el) {
            // 要素が出現、表示された後の状態を定義
        },
        enterCanselled: function(el) {
            // 要素が出現、表示するアニメーションをキャンセルされた時の状態を定義
        },
        beforeLeave: function(el) {
            // 要素が消滅、非表示される前の状態をここで定義
        },
        leave: function(el, done) {
            // 要素が消滅、非表示にされるアニメーションの実行
            // アニメーションが完了したら done コールバックを呼び出す
        },
        afterLeave: function(el) {
            // 要素が消滅、非表示されるアニメーションが完了した後の状態を定義
        },
        leaveCancelled: function(el) {
            // 要素が消滅、非表示されるアニメーションがキャンセルされた時の状態を定義
        },
    },
}).mount("#app")
