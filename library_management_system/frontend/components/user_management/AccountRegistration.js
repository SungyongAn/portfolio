// 新規アカウント登録
const AccountRegistration = {
    props: ['login-user-school'],
    emits: ['back-to-management'],
    data() {
        return {
            schools: ['A校', 'B校', 'C校', 'D校', 'E校'], // 学校の選択肢を定義
            forms: [], // 登録ユーザー情報初期値は空,resetFormsで内容を設定
            error: '',
            success: '',
            isLoading: false,
            registeredUsers: [] // 登録されたユーザー情報を保存
        };
    },
    
    created() {
        // 初回ロード時に登録初期化
        this.resetForms();
    },

    methods: {
        // 新規ユーザー情報登録項目の設定
        resetForms() {
            const currentYear = new Date().getFullYear();
            this.forms = [
                {
                    userId: '',
                    studentName: '',
                    admissionYear: currentYear,
                    graduationYear: currentYear + 3,
                    email: '',
                    schoolName: this.loginUserSchool || "" // ← ログイン者の所属校を初期値に
                }
            ];
        },

        // 新しい行を追加
        addRow() {
            const currentYear = new Date().getFullYear();
            this.forms.push({
                userId: '',
                studentName: '',
                admissionYear: currentYear,
                graduationYear: currentYear + 3,
                email: '',
                schoolName: this.loginUserSchool || "" // ← 初期値をログイン者の所属校
            });
        },
        
        // 指定した行を削除
        removeRow(index) {
            if (this.forms.length > 1) {
                this.forms.splice(index, 1);
            }
        },
        
    async handleSubmit() {
        this.isLoading = true;
        this.error = '';
        this.success = '';
        try {
            // 入力チェック
            if (!this.validateAllForms()) return;
                
            // 登録処理
            const result = await this.registerAccounts();
            if (result.success) {
                // 登録成功
                this.registeredUsers = result.users || [];
                this.success = result.message || '登録が完了しました';
                this.resetForms();
            } else {
                // 登録失敗（既存ユーザーなど）
                this.registeredUsers = result.users || [];
                this.error = result.message || '登録に失敗しました';
            }
        } catch (error) {
            console.error(error);
            this.error = error.response?.data?.detail || '登録中に予期せぬエラーが発生しました';
        } finally {
            this.isLoading = false;
        }
    },

    validateAllForms() {
        for (let i = 0; i < this.forms.length; i++) {
            const form = this.forms[i];
            const rowNumber = i + 1;
            
            if (!form.userId.trim()) {
                this.error = `${rowNumber}行目：ユーザーIDを入力してください。`;
                return false;
            }
            
            if (!form.studentName.trim()) {
                this.error = `${rowNumber}行目：生徒の名前を入力してください。`;
                return false;
            }
                
            if (!form.admissionYear) {
                this.error = `${rowNumber}行目：入学年を入力してください。`;
                return false;
            }
            
            if (!form.graduationYear) {
                this.error = `${rowNumber}行目：卒業予定年を入力してください。`;
                return false;
            }

            if (form.graduationYear <= form.admissionYear) {
                this.error = `${rowNumber}行目：卒業予定年は入学年より後の年を入力してください。`;
                return false;
            }
                
            if (!form.email.trim()) {
                this.error = `${rowNumber}行目：メールアドレスを入力してください。`;
                return false;
            }

            if (!this.isValidEmail(form.email)) {
                this.error = `${rowNumber}行目：正しいメールアドレス形式で入力してください。`;
                return false;
            }
                
            if (!form.schoolName.trim()) {
                this.error = `${rowNumber}行目：学校名を入力してください。`;
                return false;
            }
                
            // 重複チェック（ユーザーID）
            for (let j = i + 1; j < this.forms.length; j++) {
                if (form.userId === this.forms[j].userId && form.userId.trim() !== '') {
                    this.error = `${rowNumber}行目と${j + 1}行目：ユーザーIDが重複しています。`;
                    return false;
                }
            }
                
            // 重複チェック（メールアドレス）
            for (let j = i + 1; j < this.forms.length; j++) {
                if (form.email === this.forms[j].email && form.email.trim() !== '') {
                    this.error = `${rowNumber}行目と${j + 1}行目：メールアドレスが重複しています。`;
                    return false;
                }
            }
        }
        return true;
    },
        
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },
        
    async registerAccounts() {
        try {
            const payload = {
                user_id: this.forms.map(f => f.userId),
                username: this.forms.map(f => f.studentName),
                admission_year: this.forms.map(f => f.admissionYear),
                graduation_year: this.forms.map(f => f.graduationYear),
                email: this.forms.map(f => f.email),
                affiliation: this.forms.map(f => f.schoolName)
            };

            const response = await axios.post('http://127.0.0.1:8000/account-management/users-register', payload);

            console.log('登録結果:', response.data);
            return response.data;
        } catch (error) {
            console.error(error);
            throw new Error(error.response?.data?.detail || '登録中にエラーが発生しました');
        }
    }
},

    template: `
        <div class="container-fluid">
            <div class="row">
                <div class="col-12">
                    <div class="d-flex justify-content-between align-items-center mb-4">
                        <h2>新規アカウント登録</h2>
                        <button @click="$emit('back-to-management')" class="btn btn-secondary">
                            戻る
                        </button>
                    </div>
                    
                    <div class="row justify-content-center">
                        <div class="col-12">
                            <div class="card">
                                <div class="card-body">
                                    <!-- エラーメッセージ -->
                                    <div v-if="error" class="alert alert-danger" role="alert">
                                        {{ error }}
                                    </div>
                                    
                                    <!-- 成功メッセージと登録詳細 -->
                                    <div v-if="success && registeredUsers.length > 0" class="alert alert-success" role="alert">
                                        <h5 class="mb-3">{{ success }}</h5>
                                        <div class="table-responsive">
                                            <table class="table table-sm table-bordered">
                                                <thead class="table-light">
                                                    <tr>
                                                        <th>ユーザーID</th>
                                                        <th>名前</th>
                                                        <th>入学年</th>
                                                        <th>卒業予定年</th>
                                                        <th>メールアドレス</th>
                                                        <th>所属校</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr v-for="user in registeredUsers" :key="user.userId">
                                                        <td>{{ user.userId }}</td>
                                                        <td>{{ user.username }}</td>
                                                        <td>{{ user.admission_year }}</td>
                                                        <td>{{ user.graduation_year }}</td>
                                                        <td>{{ user.email }}</td>
                                                        <td>{{ user.affiliation }}</td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                        <small class="text-muted">※ 初回ログイン時にパスワードの設定が必要です</small>
                                    </div>
                                    
                                    <form @submit.prevent="handleSubmit">
                                        <!-- タイトル行 -->
                                        <div class="row mb-2 fw-bold">
                                            <div class="col-1"></div>
                                            <div class="col-2">
                                                ユーザーID
                                            </div>
                                            <div class="col-2">
                                                生徒の名前
                                            </div>
                                            <div class="col-1">
                                                入学年（西暦）
                                            </div>
                                            <div class="col-1">
                                                卒業予定年
                                            </div>
                                            <div class="col-2">
                                                メールアドレス
                                            </div>
                                            <div class="col-2">
                                                学校名
                                            </div>
                                            <div class="col-1"></div>
                                        </div>
                                        
                                        <!-- 動的入力行 -->
                                        <div v-for="(form, index) in forms" :key="index" class="row mb-2">
                                            <div class="col-1">
                                                <span class="badge bg-secondary">{{ index + 1 }}</span>
                                            </div>
                                            <div class="col-2">
                                                <input 
                                                    type="text" 
                                                    class="form-control" 
                                                    v-model="form.userId"
                                                    required
                                                    placeholder="ユーザーID">
                                            </div>
                                            <div class="col-2">
                                                <input 
                                                    type="text" 
                                                    class="form-control" 
                                                    v-model="form.studentName"
                                                    required
                                                    placeholder="生徒の名前">
                                            </div>
                                            <div class="col-1">
                                                <input 
                                                    type="number" 
                                                    class="form-control" 
                                                    v-model="form.admissionYear"
                                                    required
                                                    min="2020"
                                                    max="2100">
                                            </div>
                                            <div class="col-1">
                                                <input 
                                                    type="number" 
                                                    class="form-control" 
                                                    v-model="form.graduationYear"
                                                    required
                                                    min="2020"
                                                    max="2100">
                                            </div>
                                            <div class="col-2">
                                                <input 
                                                    type="email" 
                                                    class="form-control" 
                                                    v-model="form.email"
                                                    required
                                                    placeholder="example@example.com">
                                            </div>
                                            
                                            <div class="col-2">
                                                <!-- 所属校セレクトボックス -->
                                                <select v-model="form.schoolName" class="form-select">
                                                    <option v-for="school in schools" :key="school" :value="school">
                                                    {{ school }}
                                                    </option>
                                                </select>
                                            </div>
                                            <div class="col-1">
                                                <button 
                                                    type="button" 
                                                    class="btn btn-danger btn-sm"
                                                    @click="removeRow(index)"
                                                    :disabled="forms.length === 1"
                                                    title="この行を削除">
                                                    ×
                                                </button>
                                            </div>
                                        </div>
                                        
                                        <!-- 行追加ボタン -->
                                        <div class="row mb-4">
                                            <div class="col-12">
                                                <button 
                                                    type="button" 
                                                    class="btn btn-success btn-sm"
                                                    @click="addRow">
                                                    + 行を追加
                                                </button>
                                            </div>
                                        </div>
                                        
                                        <!-- 登録ボタン（右下） -->
                                        <div class="row">
                                            <div class="col-12 text-end">
                                                <button 
                                                    type="submit" 
                                                    class="btn btn-primary btn-lg"
                                                    :disabled="isLoading">
                                                    <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                                                    {{ isLoading ? '登録中...' : forms.length + '件を登録' }}
                                                </button>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `
};
