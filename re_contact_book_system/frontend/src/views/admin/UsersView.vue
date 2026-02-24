<template>
  <div class="container-fluid mt-4">
    <!-- フィルター -->
    <div class="row mb-3">
      <div class="col-md-3">
        <select v-model="filters.role" class="form-select" @change="fetchUsers">
          <option value="">全ロール</option>
          <option value="student">生徒</option>
          <option value="teacher">教師</option>
        </select>
      </div>
      <div class="col-md-6">
        <input
          v-model="filters.search"
          type="text"
          class="form-control"
          placeholder="名前またはメールアドレスで検索"
          @input="debounceSearch"
        />
      </div>
      <div class="col-md-3 d-flex justify-content-end align-items-center">
        <router-link to="/admin/users/create" class="btn btn-primary">
          <i class="bi bi-plus-circle"></i>
          新規ユーザー作成
        </router-link>
      </div>
    </div>

    <!-- ローディング -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">読み込み中...</span>
      </div>
    </div>

    <!-- エラー表示 -->
    <div v-else-if="error" class="alert alert-danger">
      <i class="bi bi-exclamation-triangle"></i>
      {{ error }}
    </div>

    <!-- ユーザー一覧テーブル -->
    <div v-else class="row">
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead class="table-light">
                  <tr>
                    <th>ID</th>
                    <th>名前</th>
                    <th>メールアドレス</th>
                    <th>ロール</th>
                    <th>クラス/担当</th>
                    <th>登録日</th>
                    <th class="text-center">操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="user in users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>
                      <strong>{{ user.name }}</strong>
                    </td>
                    <td>{{ user.email }}</td>
                    <td>
                      <span class="badge" :class="getRoleBadgeClass(user.displayRole)">
                        {{ user.displayRole }}
                      </span>
                    </td>
                    <td>
                      <span v-if="user.displayRole === '担任' || user.displayRole === '生徒'">
                        {{ user.displayGrade }}年{{ user.displayClass }}
                      </span>
                      <span v-else-if="user.displayRole === '学年主任'">
                        {{ user.displayGrade }}年主任
                      </span>
                      <span v-else class="text-muted">未割当</span>
                    </td>
                    <td>{{ formatDate(user.created_at) }}</td>
                    <td class="text-center">
                      <div class="btn-group btn-group-sm" role="group">
                        <router-link
                          :to="`/admin/users/${user.id}/edit`"
                          class="btn btn-outline-primary"
                          title="編集"
                        >
                          <i class="bi bi-pencil"></i>
                        </router-link>
                        <button
                          @click="confirmDelete(user)"
                          class="btn btn-outline-danger"
                          title="削除"
                          :disabled="user.id === currentUserId"
                        >
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="users.length === 0">
                    <td colspan="7" class="text-center text-muted py-4">
                      ユーザーが見つかりません
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- ページネーション（将来実装） -->
            <div v-if="totalPages > 1" class="d-flex justify-content-center mt-3">
              <nav>
                <ul class="pagination">
                  <!-- TODO: ページネーション実装 -->
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 削除確認モーダル -->
    <div
      class="modal fade"
      id="deleteModal"
      tabindex="-1"
      aria-hidden="true"
      ref="deleteModal"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">ユーザー削除の確認</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              以下のユーザーを削除してもよろしいですか？
            </p>
            <div v-if="userToDelete" class="alert alert-warning">
              <strong>{{ userToDelete.name }}</strong> ({{ userToDelete.email }})
            </div>
            <p class="text-danger">
              <i class="bi bi-exclamation-triangle"></i>
              この操作は取り消せません。
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              キャンセル
            </button>
            <button
              type="button"
              class="btn btn-danger"
              @click="deleteUser"
              :disabled="deleting"
            >
              <span v-if="deleting" class="spinner-border spinner-border-sm me-2"></span>
              削除する
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { adminAPI } from '@/services/adminService'
import { authAPI } from '@/services/authService'
import { Modal } from 'bootstrap'

const router = useRouter()
const authStore = useAuthStore()

// State
const users = ref([])
const loading = ref(false)
const error = ref(null)
const filters = ref({
  role: '',
  search: ''
})
const currentUserId = computed(() => authStore.userId)
const totalPages = ref(1)

// 削除関連
const deleteModal = ref(null)
const deleteModalInstance = ref(null)
const userToDelete = ref(null)
const deleting = ref(false)

// ユーザー取得
const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    const params = {}
    if (filters.value.role) params.role = filters.value.role
    if (filters.value.search) params.search = filters.value.search

    const response = await adminAPI.getUsers(params)

    // 教師の primary_assignment から displayRole を追加
    users.value = response.data.map(user => {
      let displayRole = ''
      let displayGrade = null
      let displayClass = null

      if (user.role === 'teacher' && user.primary_assignment) {
        switch(user.primary_assignment.assignment_type) {
          case 'homeroom':
            displayRole = '担任'
            break
          case 'grade_head':
            displayRole = '学年主任'
            break
          case 'subject':
            displayRole = '教科担当'
            break
          default:
            displayRole = '教師'
        }
        displayGrade = user.primary_assignment.grade_number
        displayClass = user.primary_assignment.class_name

      } else if (user.role === 'student') {
        displayRole = '生徒'
        displayGrade = user.student_class?.grade_number ?? null
        displayClass = user.student_class?.class_name ?? null

      } else if (user.role === 'admin') {
        displayRole = '管理者'
      } else {
        displayRole = user.role
      }

      return {
        ...user,
        displayRole,
        displayGrade,
        displayClass
      }
    })
  } catch (err) {
    console.error('ユーザー取得エラー:', err)
    error.value = 'ユーザー情報の取得に失敗しました'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // accessToken が無ければ refresh を試みる
  if (!authStore.accessToken) {
    const refreshed = await authAPI.refreshAccessToken()
    if (!refreshed) {
      // 未ログイン扱い → ログイン画面へ
      router.push('/login')
      return
    }
  }

  // 認証が確定してから取得
  await fetchUsers()

  // Bootstrapモーダルの初期化
  deleteModalInstance.value = new Modal(deleteModal.value)
})

// 検索のデバウンス
let searchTimeout = null
const debounceSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    fetchUsers()
  }, 500)
}

// ロールバッジのクラス
const getRoleBadgeClass = (displayrole) => {
  const classes = {
    admin: 'bg-danger',
    担任: 'bg-primary',
    教科担当: 'bg-primary',
    学年主任: 'bg-primary',
    生徒: 'bg-success'
  }
  return classes[displayrole] || 'bg-secondary'
}


// 日付フォーマット
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

// 削除確認
const confirmDelete = (user) => {
  userToDelete.value = user
  deleteModalInstance.value.show()
}

// ユーザー削除
const deleteUser = async () => {
  if (!userToDelete.value) return

  deleting.value = true
  try {
    await adminAPI.deleteUser(userToDelete.value.id)
    deleteModalInstance.value.hide()
    userToDelete.value = null
    // リストを再取得
    await fetchUsers()
  } catch (err) {
    console.error('削除エラー:', err)
    alert('ユーザーの削除に失敗しました')
  } finally {
    deleting.value = false
  }
}

</script>

<style scoped>
.table th {
  white-space: nowrap;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
}
</style>