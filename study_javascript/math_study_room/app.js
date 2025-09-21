Vue.createApp({
    data() {
        return {
            selectedNumberType: '', 
            selectedIntegerArithmetic: '',
            selectedIntegerDigits: '',
            selectedRealArithmetic: '',      
            selectedRealDigits: '',
            numQuestions: '',
            userAnswers: [],
            checkAnswersResults: [],
            // 以下はbackendから問題を受ける用
            questions: [], 
            answers: [],
        }
    },
    computed: {
        hasQuestions: function() {
            return this.questions.length > 0
        },
        hasCheckAnswersResults: function(){
            return this.checkAnswersResults.length > 0
        },
    },
    methods: {
        async createQuestions() {

            // 問題作成時に解答欄などをリセット
            this.userAnswers = [];
            this.checkAnswersResults = [];
            this.questions = [];
            this.answers = [];

            // 条件をまとめる
            const payload = {
                type: this.selectedNumberType,
                arithmetic: this.selectedNumberType === 'integer' 
                    ? this.selectedIntegerArithmetic 
                    : this.selectedRealArithmetic,
                digits: parseInt(this.selectedNumberType === 'integer' 
                    ? this.selectedIntegerDigits
                    : this.selectedRealDigits),
                numquestions: parseInt(this.numQuestions)
            };

            // バックエンドに送信する想定
            try {
                const res = await fetch('http://127.0.0.1:8000/questions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const requestData = await res.json();
                this.questions = requestData.questions;
                this.answers = requestData.answers;

            } catch (err) {
                console.error("問題の取得に失敗:", err);
            }
        },
        checkAnswers(){
            this.checkAnswersResults = this.userAnswers.map((item, i) => item === this.answers[i] ? "正解" : "不正解");
        },
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
        },
    }
}).mount("#app")
