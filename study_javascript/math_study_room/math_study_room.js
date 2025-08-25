Vue.createApp({
    data() {
        return {
            selectedNumberType: '', 
            selectedIntegerArithmetic: '',
            selectedIntegerDigits: '',
            selectedRealArithmetic: '',      
            selectedRealDigits: '',
            numQuestions: ''
            questions: [] // backendから問題を受ける用
        }
    },
    methods: {
        createQuestions() {
          // 問題作成処理
        }
    },
    watch: {
        // メインの選択（整数/実数）が変わった時
        selectedNumberType(newValue, oldValue) {
            if (newValue !== oldValue) {
                // 整数の設定をリセット
                this.selectedIntegerArithmetic = null;
                this.selectedIntegerDigits = null;
                // 実数の設定をリセット
                this.selectedRealArithmetic = null;
                this.selectedRealDigits = null;
                // 出題数もリセット
                this.numQuestions = '';
            }
        }
    }
}).mount("#app")
