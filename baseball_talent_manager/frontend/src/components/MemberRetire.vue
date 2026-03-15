<template>
  <div class="container mt-4">
    <h2 class="mb-4">部員退部・引退処理</h2>

    <!-- 成功メッセージ -->
    <div v-if="successMessage" class="alert alert-success">
      <i class="bi bi-check-circle me-2"></i>
      {{ successMessage }}
    </div>

    <!-- 部員一覧テーブル -->
    <div class="table-responsive">
      <table class="table table-hover align-middle">
        <thead class="table-light">
          <tr>
            <th>氏名</th>
            <th>学年</th>
            <th>ステータス</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="member in activeMembers" :key="member.user_id">
            <td>{{ member.name }}</td>
            <td>{{ member.grade }}年</td>
            <td>
              <span class="badge bg-success">在籍中</span>
            </td>
            <td>
              <div class="d-flex gap-2">
                <button
                  class="btn btn-sm btn-outline-warning"
                  @click="openModal(member, 'retired')"
                >
                  引退
                </button>
                <button
                  class="btn btn-sm btn-outline-danger"
                  @click="openModal(member, 'withdrawn')"
                >
                  退部
                </button>
              </div>
            </td>
          </tr>
          <tr v-if="activeMembers.length === 0">
            <td colspan="4" class="text-center text-muted">
              在籍中の部員はいません
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 確認モーダル -->
    <div
      v-if="showModal"
      class="modal d-block"
      tabindex="-1"
      style="background-color: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">処理の確認</h5>
          </div>
          <div class="modal-body">
            <p>
              <strong>{{ selectedMember?.name }}</strong
              >さんを
              <strong
                :class="
                  actionType === 'retired' ? 'text-warning' : 'text-danger'
                "
              >
                {{ actionType === "retired" ? "引退" : "退部" }}
              </strong>
              として処理します。よろしいですか？
            </p>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="showModal = false"
            >
              キャンセル
            </button>
            <button
              type="button"
              :class="
                actionType === 'retired' ? 'btn btn-warning' : 'btn btn-danger'
              "
              @click="handleProcess"
            >
              {{ actionType === "retired" ? "引退処理" : "退部処理" }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { updateUserStatus, getUsers } from "@/services/userService.js";

const allMembers = ref([]);

onMounted(async () => {
  const res = await getUsers("member");
  allMembers.value = res.data.users;
});

// activeな部員のみ表示
const activeMembers = computed(() =>
  allMembers.value.filter((m) => m.status === "active"),
);

// モーダル制御
const showModal = ref(false);
const selectedMember = ref(null);
const actionType = ref(""); // 'retired' or 'withdrawn'
const successMessage = ref("");

const openModal = (member, type) => {
  selectedMember.value = member;
  actionType.value = type;
  showModal.value = true;
};

const handleProcess = async () => {
  const label = actionType.value === "retired" ? "引退" : "退部";
  await updateUserStatus(selectedMember.value.user_id, actionType.value);
  // 再取得
  const res = await getUsers("member");
  allMembers.value = res.data.users;
  successMessage.value = `${selectedMember.value.name}さんを${label}処理しました`;
  showModal.value = false;
};
</script>
