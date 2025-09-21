Vue.createApp({
    data: function() {
        return {
            todoTitle: "",
            todoDescription: "",
            todoCategories: [],
            categories: [],
            categoryName: "",
        }
    },

    computed: {
        // カテゴリー未入力、入力したカテゴリーの有無を確認
        canCreateCategory: function() {
            return this.categoryName !== "" && !this.existsCategory
        },
        existsCategory: function() {
            const categoryName = this.categoryName
            // カテゴリリスト内に入力したカテゴリがあるか確認
            return this.categories.indexOf(categoryName) !== -1
        },
    },

    methods: {
        createCategory: function() {
            if (!this.canCreateCategory) {
                return
            }
            this.categories.push(this.categoryName)
            
            // 入力欄の初期化
            this.categoryName = ""
        },
    },

        created: function() {
        try {
            // ブラウザのストレージにアクセスして categories の情報を取り出す。
            const categories = window.localStorage.getItem("categories")

            if (categories) {
                const parsedCategories = JSON.parse(categories)
                this.categories = Array.isArray(parsedCategories) ? parsedCategories : []
            }
            
        // エラー時は空の配列で初期化
        } catch (error) {
            // console.error("LocalStorage読み込みエラー:", error)
            this.categories = []
        }
    },
}).mount("#app")
