Vue.createApp({
    data: function() {
        return {
            isShow: false,
        }
    },
    methods: {
        showAndFade() {
            this.isShow = true;
            setTimeout(() => {
                this.isShow = false;
            }, 1);
        }
    }
}).mount("#app")
