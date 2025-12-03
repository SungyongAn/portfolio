const LoginForm = {
  data() {
    return {
      loginData: {
        id: '',
        name: '',
        password: ''
      },
      errorMessage: '',
      isLoading: false,
      showPassword: false
    };
  },
  methods: {
    async handleLogin() {
      this.errorMessage = '';
      this.isLoading = true;

      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/auth/login',
          this.loginData
        );
        console.log('Full response:', response);
        console.log('Access token directly:', response.data.data.access_token);

        if (response.data.success) {
          // トークンの処理を先に行う
          const token = response.data.data.access_token;
          console.log('Token before storage:', token);
          
          if (token) {
            // トークンを保存
            sessionStorage.setItem('access_token', token);
            
            // axiosのデフォルトヘッダーに設定
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            console.log('Saved token:', token);
          } else {
            console.warn('No access_token in response');
            this.errorMessage = 'トークンが取得できませんでした';
            return;
          }
          // ユーザーデータの設定
          const userData = {
            id: response.data.data.id, 
            role: response.data.data.role,
            grade: response.data.data.grade,
            className: response.data.data.class_name,
            fullName: response.data.data.name,
            isTeacher: response.data.data.role === 'teacher',
            teacherRole: response.data.data.teacher_role?.code || null,
            isGradeLeader: response.data.data.teacher_role?.code === 'grade_leader', // 学年主任
            isHomeroomTeacher: response.data.data.teacher_role?.code === 'homeroom', // 担任
            isAssistantTeacher: response.data.data.teacher_role?.code === 'assistant_homeroom',  // 副担任
            isSubjectTeacher: response.data.data.teacher_role?.code === 'subject_teacher', // 教科担当
            isAdmin: response.data.data.role === 'admin',
            status: response.data.data.status,
            enrollmentYear: response.data.data.enrollment_year || 0,
            graduationYear: response.data.data.graduation_year || 0
          };

          // ユーザー情報をemit
          this.$emit('login', userData);
          
          // フォームをリセット（resetFormメソッドがあれば）
          this.loginData = {
            id: '',
            name: '',
            password: ''
          };
        } else {
          this.errorMessage = response.data.message || 'ログインに失敗しました';
        }
      } catch (error) {
        console.error('Login error:', error);
        this.errorMessage = error.response?.data?.detail || 'ログイン処理中にエラーが発生しました';
      } finally {
        this.isLoading = false;
      }
    }
  },
  template: `
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card shadow">
            <div class="card-header bg-primary text-white">
              <h4 class="mb-0">連絡帳システム ログイン</h4>
            </div>
            <div class="card-body">
              <div v-if="errorMessage" class="alert alert-danger">
                {{ errorMessage }}
              </div>
              
              <form @submit.prevent="handleLogin">
                <div class="mb-3">
                  <label for="id" class="form-label">ID</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="id"
                    v-model="loginData.id" 
                    required
                    :disabled="isLoading">
                </div>
                
                <div class="mb-3">
                  <label for="name" class="form-label">名前</label>
                  <input 
                    type="text" 
                    class="form-control" 
                    id="name"
                    v-model="loginData.name" 
                    required
                    :disabled="isLoading">
                </div>
                
                <div class="mb-3">
                  <label for="password" class="form-label">パスワード</label>
                  <input 
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control" 
                    id="password"
                    v-model="loginData.password" 
                    required
                    :disabled="isLoading">
                  
                  <!-- チェックボックス -->
                  <div class="form-check mt-2">
                    <input 
                      type="checkbox" 
                      class="form-check-input" 
                      id="showPassword"
                      v-model="showPassword">
                    <label for="showPassword" class="form-check-label">パスワードを表示</label>
                  </div>
                </div>
                
                
                <button 
                  type="submit" 
                  class="btn btn-primary w-100" 
                  :disabled="isLoading">
                  <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                  ログイン
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
};
