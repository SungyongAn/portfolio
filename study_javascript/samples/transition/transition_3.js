Vue.createApp({
    data: function() {
        return {
            filterDone: false,
            items: [
                {
                    title: "タイトル - 1",
                    done: false, // 消える
                },
                {
                    title: "タイトル - 2",
                    done: true, // 消えない
                },
                {
                    title: "タイトル - 3",
                    done: true, // 消えない
                },
                {
                    title: "タイトル - 4",
                    done: false, // 消える
                },
            ],
        }
    },

    computed: {
        filteredItems: function() {
            if(this.filterDone) {
                return this.items.filter(function(item) {
                    return item.done
                })
            }
            return this.items
        },
    },
}).mount("#app")
