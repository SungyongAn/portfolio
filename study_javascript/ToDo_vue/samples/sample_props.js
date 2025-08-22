const countUpButton = {
    template: "#btn-template",
    props: {
        count: {
            type: Number,
            required: true,
        },
    },
    methods: {
        onClick: function () {
            // this.$emit("count-up", this.count + 1)
            this.$emit("update:count", this.count + 1)
        },
    },
}

Vue.createApp({
    data: function() {
        return {
            count: 0,
        }
    },
    components: {
        "count-up-button": countUpButton,
    },
    // methods: {
    //     countUp: function(nextCount) {
    //         this.count = nextCount
    //     },
    // },
}).mount("#app")
