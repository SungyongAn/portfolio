Vue.createApp({
    data: function() {
        return {
            todoTitle: "",
            todoDescription: "",
            todoCategories: [],
            selectCategoly: "",
            hideDoneToDo: false,
            searchWord: "",
            order: "desc",
            categoryName: "",
        }
    },
    computed: {
        canCreateToDo: function() {
            return this.todoTitle !==""
        },
        canCreateCategory: function () {
            return this.categoryName !== ""
        }
    },
    methods: {
        createTodo: function () {
            if (!this.canCreateToDo) {
                return
            }

            // トゥドゥタスクを追加する処理
            this.todoTitle = ""
            this.todoDescription = ""
            this.todoCategories = []
        },
    createCategory: function() {
        if (!this.canCreateCategory) {
                return
            }
            this.categoryName = ""
        },
    },
}).mount("#app")
