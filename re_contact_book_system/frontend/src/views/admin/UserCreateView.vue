<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <!-- ヘッダー -->
        <div class="d-flex align-items-center mb-4">
          <button @click="router.back()" class="btn btn-outline-secondary me-3">
            <i class="bi bi-arrow-left"></i>
          </button>
          <h1 class="mb-0">
            <i class="bi bi-person-plus"></i>
            新規ユーザー作成
          </h1>
        </div>

        <!-- エラー表示 -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show">
          <i class="bi bi-exclamation-triangle"></i>
          {{ error }}
          <button type="button" class="btn-close" @click="error = null"></button>
        </div>

        <!-- フォーム -->
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <form @submit.prevent="handleSubmit">
              <!-- ロール選択 -->
              <div class="mb-3">
                <label for="role" class="form-label">
                  ロール <span class="text-danger">*</span>
                </label>
                <select
                  id="role"
                  v-model="form.role"
                  class="form-select"
                  :class="{ 'is-invalid': errors.role }"
                  required
                >
                  <option value="">選択してください</option>
                  <option value="student">生徒</option>
                  <option value="teacher">教師</option>
                  <option value="admin">管理者</option>
                </select>
                <div v-if="errors.role" class="invalid-feedback">
                  {{ errors.role }}
                </div>
              </div>

              <!-- 名前 -->
              <div class="mb-3">
                <label for="name" class="form-label">
                  氏名 <span class="text-danger">*</span>
                </label>
                <input
                  id="name"
                  v-model="form.name"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.name }"
                  placeholder="山田 太郎"
                  required
                />
                <div v-if="errors.name" class="invalid-feedback">
                  {{ errors.name }}
                </div>
              </div>

              <!-- メールアドレス -->
              <div class="mb-3">
                <label for="email" class="form-label">
                  メールアドレス <span class="text-danger">*</span>
                </label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  class="form-control"
                  :class="{ 'is-invalid': errors.email }"
                  placeholder="yamada.taro@school.ac.jp"
                  required
                />
                <div v-if="errors.email" class="invalid-feedback">
                  {{ errors.email }}
                </div>
                <div class="form-text">
                  @school.ac.jp のメールアドレスを入力してください
                </div>
              </div>

              <!-- パスワード -->
              <div class="mb-3">
                <label for="password" class="form-label">
                  パスワード <span class="text-danger">*</span>
                </label>
                <div class="input-group">
                  <input
                    id="password"
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control"
                    :class="{ 'is-invalid': errors.password }"
                    placeholder="8文字以上"
                    required
                  />
                  <button
                    class="btn btn-outline-secondary"
                    type="button"
                    @click="showPassword = !showPassword"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                  <div v-if="errors.password" class="invalid-feedback">
                    {{ errors.password }}
                  </div>
                </div>
                <div class="form-text">
                  8文字以上の英数字を含むパスワードを設定してください
                </div>
              </div>

              <!-- 生徒の場合：クラス割当 -->
              <div v-if="form.role === 'student'" class="mb-3">
                <label class="form-label">クラス割当（任意）</label>
                <div class="row">
                  <div class="col-md-6">
                    <select v-model="classAssignment.gradeId" class="form-select">
                      <option value="">学年を選択</option>
                      <option value="1">1年</option>
                      <option value="2">2年</option>
                      <option value="3">3年</option>
                    </select>
                  </div>
                  <div class="col-md-6">
                    <select v-model="classAssignment.className" class="form-select">
                      <option value="">クラスを選択</option>
                      <option value="A組">A組</option>
                      <option value="B組">B組</option>
                      <option value="C組">C組</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- 教師の場合：担当クラス -->
              <div v-if="form.role === 'teacher'" class="mb-3">
                <label class="form-label">担当設定（任意）</label>
                <div class="form-check">
                  <input
                    id="isHomeroom"
                    v-model="teacherAssignment.isHomeroom"
                    class="form-check-input"
                    type="checkbox"
                  />
                  <label class="form-check-label" for="isHomeroom">
                    担任として登録
                  </label>
                </div>
                <div v-if="teacherAssignment.isHomeroom" class="mt-2">
                  <div class="row">
                    <div class="col-md-6">
                      <select v-model="teacherAssignment.gradeId" class="form-select">
                        <option value="">学年を選択</option>
                        <option value="1">1年</option>
                        <option value="2">2年</option>
                        <option value="3">3年</option>
                      </select>
                    </div>
                    <div class="col-md-6">
                      <select v-model="teacherAssignment.className" class="form-select">
                        <option value="">クラスを選択</option>
                        <option value="A組">A組</option>
                        <option value="B組">B組</option>
                        <option value="C組">C組</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>

              <!-- ボタン -->
              <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-4">
                <button
                  type="button"
                  class="btn btn-outline-secondary"
                  @click="router.back()"
                >
                  キャンセル
                </button>
                <button
                  type="submit"
                  class="btn btn-primary"
                  :disabled="submitting"
                >
                  <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                  作成する
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI } from '@/services/api'

const router = useRouter()

// フォームデータ
const form = reactive({
  role: '',
  name: '',
  email: '',
  password: ''
})

const classAssignment = reactive({
  gradeId: '',
  className: ''
})

const teacherAssignment = reactive({
  isHomeroom: false,
  gradeId: '',
  className: ''
})

// State
const showPassword = ref(false)
const submitting = ref(false)
const error = ref(null)
const errors = ref({})

// バリデーション
const validate = () => {
  errors.value = {}

  if (!form.role) {
    errors.value.role = 'ロールを選択してください'
  }

  if (!form.name || form.name.trim().length === 0) {
    errors.value.name = '氏名を入力してください'
  }

  if (!form.email) {
    errors.value.email = 'メールアドレスを入力してください'
  } else if (!form.email.endsWith('@school.ac.jp')) {
    errors.value.email = '@school.ac.jp のメールアドレスを入力してください'
  }

  if (!form.password) {
    errors.value.password = 'パスワードを入力してください'
  } else if (form.password.length < 8) {
    errors.value.password = 'パスワードは8文字以上である必要があります'
  }

  return Object.keys(errors.value).length === 0
}

// 送信処理
const handleSubmit = async () => {
  if (!validate()) {
    return
  }

  submitting.value = true
  error.value = null

  try {
    // ユーザー作成
    const userData = {
      role: form.role,
      name: form.name,
      email: form.email,
      password: form.password
    }

    const response = await adminAPI.createUser(userData)
    const userId = response.data.id

    // クラス割当（生徒の場合）
    if (form.role === 'student' && classAssignment.gradeId && classAssignment.className) {
      await adminAPI.assignStudentToClass({
        student_id: userId,
        grade_id: classAssignment.gradeId,
        class_name: classAssignment.className
      })
    }

    // 担当割当（教師の場合）
    if (form.role === 'teacher' && teacherAssignment.isHomeroom && teacherAssignment.gradeId) {
      await adminAPI.assignTeacherToClass({
        teacher_id: userId,
        grade_id: teacherAssignment.gradeId,
        class_name: teacherAssignment.className,
        is_primary: true
      })
    }

    // 成功したら一覧へ
    router.push('/admin/users')
  } catch (err) {
    console.error('ユーザー作成エラー:', err)
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'ユーザーの作成に失敗しました'
    }
  } finally {
    submitting.value = false
  }
}
</script>