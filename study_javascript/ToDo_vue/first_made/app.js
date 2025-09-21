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
                        selectedCategory === "" || 
                        (Array.isArray(todo.categories) && todo.categories.indexOf(selectedCategory) !== -1)
                    )
                })
                .filter(function(todo) {
                    if(hideDoneTodo) {
                        return !todo.done
                    }
                    return true
                })
                .filter(function(todo) {
                    // 安全なnullチェックを追加
                    if (!searchWord) return true;
                    
                    const title = todo.title || "";
                    const description = todo.description || "";
                    
                    return (
                        title.indexOf(searchWord) !== -1 || 
                        description.indexOf(searchWord) !== -1
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
            
            // データの整合性を保証
            this.todos.push({
                id: "todo-" + Date.now(),
                title: this.todoTitle || "", // 空文字列を保証
                description: this.todoDescription || "", // 空文字列を保証
                categories: Array.isArray(this.todoCategories) ? [...this.todoCategories] : [], // 配列を保証
                dateTime: Date.now(),
                done: false,
            })

            // フォームリセット
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

        // データの正規化メソッドを追加
        normalizeTodoData: function(todo) {
            return {
                ...todo,
                title: todo.title || "",
                description: todo.description || "",
                categories: Array.isArray(todo.categories) ? todo.categories : [],
                done: Boolean(todo.done),
                dateTime: todo.dateTime || Date.now(),
                id: todo.id || "todo-" + Date.now()
            }
        }
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
