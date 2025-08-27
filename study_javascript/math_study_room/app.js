Vue.createApp({
    data() {
        return {
            selectedNumberType: '', 
            selectedIntegerArithmetic: '',
            selectedIntegerDigits: '',
            selectedRealArithmetic: '',      
            selectedRealDigits: '',
            numQuestions: '',
            questions: [], // backendから問題を受ける用
            answers: [],
        }
    },
    methods: {
        async createQuestions() {
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

                console.log("受け取った問題:", this.questions);
                console.log("受け取った問題:", this.answers);
            } catch (err) {
                console.error("問題の取得に失敗:", err);
            }
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
