Vue.createApp({
    data: function() {
        return {
            todoTitle: "",
            todoDescription: "",
            todoCategories: [],
            selectedCategory: "",
            todos: [],
            categories: [],
            hideDoneTodo: false,
            searchWord: "",
            order: "desc",
            categoryName: "",
        }
    },
    computed: {
        // タイトル未入力は除外
        canCreateTodo: function() {
            return this.todoTitle !== ""
        },
        // カテゴリー未入力、入力したカテゴリーの有無を確認
        canCreateCategory: function() {
            return this.categoryName !== "" && !this.existsCategory
        },

        existsCategory: function() {
            const categoryName = this.categoryName
            // ) !== -1 は見つけた場合はTrue、見つからない場合はFalseを返す。
            // 下記の内容だと categories に categoryName が存在するか確認
            return this.categories.indexOf(categoryName) !== -1
        },

        hasTodos: function() {
            return this.todos.length > 0
        },

        resultTodos: function() {
            const selectedCategory = this.selectedCategory
            const hideDoneTodo = this.hideDoneTodo
            const order = this.order
            const searchWord = this.searchWord

            return this.todos
                .filter(function(todo) {
                    return (
                        // 条件１ selectedCategory が空の場合
                        selectedCategory === "" 
                        // || = or
                        || 
                        // 条件２ categories の中に selectedCategory が存在する場合
                        todo.categories.indexOf(selectedCategory) !== -1
                    )
                })

                // 完了済みタスクの切り替え
                .filter(function(todo) {
                    if(hideDoneTodo) {
                        return !todo.done
                    }
                    return true
                })

                .filter(function(todo) {
                    return (
                        // タイトルに検索ワードが存在する場合
                        todo.title.indexOf(searchWord) !== -1 || 
                        // 説明に検索ワードが存在する場合
                        todo.description.indexOf(searchWord) !== -1
                    )
                })

                .sort(function(a, b) {
                    if (order === "asc") {
                        return a.dateTime - b.dateTime
                    }
                    return b.dateTime - a.dateTime
                })
            },
        },

    watch: {
        todos: {
            handler: function(next) {
                window.localStorage.setItem("todos", JSON.stringify(next))
            },
            deep: true,
        },
        categories: {
            handler: function(next) {
                window.localStorage.setItem("categories", JSON.stringify(next))
            },
            deep: true,
        },
    },

    methods: {
        createTodo: function () {
            if (!this.canCreateTodo) {
                return
            }
            this.todos.push({
                id: "todo-" + Date.now(),
                title: this.todoTitle,
                description: this.todoDescription,
                categories: this.todoCategories,
                dateTime: Date.now(),
                done: false,
            })

            // トゥドゥタスクを追加する処理
            this.todoTitle = ""
            this.todoDescription = ""
            this.todoCategories = []
        },

        createCategory: function() {
            if (!this.canCreateCategory) {
                    return
                }

                this.categories.push(this.categoryName)

                this.categoryName = ""
        },
    },

    created: function() {
        const todos = window.localStorage.getItem("todos")
        const categories = window.localStorage.getItem("categories")

        if (todos) {
            this.todos = JSON.parse(todos)
        }

        if (categories) {
            this.categories = JSON.parse(categories)
        }
    },
}).mount("#app")
