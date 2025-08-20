Vue.createApp({
    data: function() {
        return {
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
            return this.categories.indexOf(categoryName) !== -1
        },
    },

    methods: {
        createCategory: function() {
            if (!this.canCreateCategory) {
                return
            }

            this.categories.push(this.categoryName)
            this.categoryName = ""
        },
    },

    created: function() {
        try {
            const todos = window.localStorage.getItem("todos")
            const categories = window.localStorage.getItem("categories")

            if (todos) {
                const parsedTodos = JSON.parse(todos)
                // データを正規化して安全性を確保
                this.todos = parsedTodos.map(todo => this.normalizeTodoData(todo))
            }

            if (categories) {
                const parsedCategories = JSON.parse(categories)
                this.categories = Array.isArray(parsedCategories) ? parsedCategories : []
            }
            
            console.log("データ読み込み完了:", { todos: this.todos.length, categories: this.categories.length })
        } catch (error) {
            console.error("LocalStorage読み込みエラー:", error)
            // エラー時は空の配列で初期化
            this.todos = []
            this.categories = []
        }
    },
}).mount("#app")
