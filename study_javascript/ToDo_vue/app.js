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
        }
    },
}).mount("#app")
