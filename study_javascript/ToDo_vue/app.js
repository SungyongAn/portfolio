Vue.createApp({
    data: function() {
        return {
            todoTitle: "",
            todoDescription: "",
            todoCategories: [],
            selectedCategory: "",
            todos: [],
            categories: [],
            hideDoneToDo: false,
            searchWord: "",
            order: "desc",
            categoryName: "",
        }
    },
    computed: {
        // タイトル未入力は除外
        canCreateToDo: function() {
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
        hasToDos: function() {
            return this.todos.length > 0
        },
    },

    resultTodos: function() {
        const selectedCategory = this.selectedCategory
        const hideDoneToDo = this.hideDoneToDo
        const order = this.order
        const searchWord = this.searchWord
        return this.todos
        .filter(function(todo) {
            return (
                selectedCategory === "" || todo.categories.indexOf(selectedCategory) !== -1
            )
        })
        .filter(function(todo) {
            if(hideDoneToDo) {
                return !todo.done
            }
            return true
        })
        .filter(function(todo) {
            return (
                todo.title.indexOf(searchWord) !== -1 || 
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
            if (!this.canCreateToDo) {
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
