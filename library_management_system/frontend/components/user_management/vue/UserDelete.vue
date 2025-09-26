<template>
  <div class="card">
    <div class="card-body">
      <h5>検索結果（{{ searchResults.length }}件）</h5>
      <div v-if="deleteMessage" class="alert alert-info">
        {{ deleteMessage }}
      </div>
      <div class="table-responsive">
        <table class="table table-striped">
          <thead class="table-dark">
            <tr>
              <th></th>
              <th>ユーザーID</th>
              <th>ユーザー名</th>
              <th>入学年</th>
              <th>卒業予定年</th>
              <th>メールアドレス</th>
              <th>所属校</th>
              <th>権限</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in searchResults" :key="user.user_id">
              <td>
                <input
                  type="checkbox"
                  v-model="selectedUsers"
                  :value="user.user_id"
                />
              </td>
              <td>{{ user.user_id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.admission_year }}</td>
              <td>{{ user.graduation_year }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.affiliation }}</td>
              <td>
                <span
                  class="badge"
                  :class="
                    user.role === '管理者'
                      ? 'bg-danger'
                      : user.role === '司書'
                      ? 'bg-warning'
                      : user.role === '図書委員'
                      ? 'bg-info'
                      : 'bg-secondary'
                  "
                >
                  {{ user.role }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <button
        class="btn btn-danger mt-3"
        @click="handleDelete"
        :disabled="selectedUsers.length === 0 || isLoading"
      >
        削除
        <span
          v-if="isLoading"
          class="spinner-border spinner-border-sm ms-2"
        ></span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: ["searchResults"],
  data() {
    return {
      selectedUsers: [],
      deleteMessage: "",
      isLoading: false,
    };
  },
  methods: {
    async handleDelete() {
      if (this.selectedUsers.length === 0) return;
      if (!confirm(`${this.selectedUsers.length}件のユーザーを削除しますか？`))
        return;

      this.isLoading = true;
      this.deleteMessage = "";

      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/account-management/delete-users",
          {
            user_id: this.selectedUsers,
          }
        );

        if (response.data.success) {
          this.deleteMessage = `${this.selectedUsers.length}件削除しました`;
          const updatedResults = this.searchResults.filter(
            (u) => !this.selectedUsers.includes(u.user_id)
          );
          this.$emit("delete-completed", updatedResults);
          this.selectedUsers = [];
        } else {
          this.deleteMessage = "削除に失敗しました: " + response.data.message;
        }
      } catch (err) {
        console.error(err);
        this.deleteMessage = "削除中にエラーが発生しました";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
