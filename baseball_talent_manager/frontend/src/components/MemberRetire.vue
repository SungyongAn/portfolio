<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="mb-4">部員退部・引退処理</h2>

      <div class="d-flex gap-2 align-items-center">
        <!-- ソート項目 -->
        <select v-model="sortKey" class="form-select form-select-sm">
          <option value="name">部員名</option>
          <option value="grade">学年</option>
        </select>

        <!-- 昇順 / 降順 -->
        <button
          @click="toggleOrder"
          class="btn btn-outline-primary btn-sm text-nowrap"
        >
          {{ sortOrder === "asc" ? "昇順 ↑" : "降順 ↓" }}
        </button>

        <!-- 名前フィルタ -->
        <input
          v-model="filterName"
          type="text"
          placeholder="名前検索"
          class="form-control form-control-sm ms-3"
        />

        <!-- 学年フィルタ -->
        <select v-model="filterGrade" class="form-select form-select-sm">
          <option value="">学年（全て）</option>
          <option value="1">1年</option>
          <option value="2">2年</option>
          <option value="3">3年</option>
        </select>

        <!-- リセット -->
        <button
          @click="resetFilters"
          :disabled="isResetDisabled"
          class="btn btn-outline-secondary btn-sm ms-2 text-nowrap"
        >
          リセット
        </button>
      </div>
    </div>

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
          <tr v-for="member in paginatedData" :key="member.user_id">
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
          <tr v-if="paginatedData.length === 0">
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
              @click="closeModal"
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

    <!-- ページネーション -->
    <div class="d-flex justify-content-between align-items-center mt-3">
      <Pagination
        v-model="currentPage"
        :totalPages="totalPages"
        :pageSize="pageSize"
        @update:pageSize="
          pageSize = $event;
          currentPage = 1;
        "
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { updateUserStatus, getUsers } from "@/services/userService.js";
import { useRoute, useRouter } from "vue-router";
import { usePagination } from "@/composables/usePagination";
import Pagination from "@/components/Pagination.vue";

const route = useRoute();
const router = useRouter();
const allMembers = ref([]);

onMounted(async () => {
  try {
    const res = await getUsers("member");
    allMembers.value = res.data.users;
  } catch (e) {
    console.error("ユーザー取得失敗", e);
  }
});

// activeな部員のみ表示
const activeMembers = computed(() =>
  allMembers.value.filter((m) => m.status === "active"),
);

// モーダル制御
const showModal = ref(false);
const selectedMember = ref(null);
const actionType = ref("");
const successMessage = ref("");

const closeModal = () => {
  showModal.value = false;
  selectedMember.value = null;
  actionType.value = "";
};

const openModal = (member, type) => {
  selectedMember.value = member;
  actionType.value = type;
  showModal.value = true;
};

const handleProcess = async () => {
  try {
    const label = actionType.value === "retired" ? "引退" : "退部";

    await updateUserStatus(selectedMember.value.user_id, actionType.value);

    const res = await getUsers("member");
    allMembers.value = res.data.users;

    successMessage.value = `${selectedMember.value.name}さんを${label}処理しました`;
    closeModal();
  } catch (e) {
    console.error("更新失敗", e);
  }
};

// ソート関数化（可読性向上）
const compareValues = (a, b, key, order = "asc") => {
  const valA = a[key];
  const valB = b[key];

  // 数値判定
  if (!isNaN(valA) && !isNaN(valB)) {
    return order === "asc"
      ? Number(valA) - Number(valB)
      : Number(valB) - Number(valA);
  }

  // 文字列判定（日本語対応）
  return order === "asc"
    ? String(valA).localeCompare(String(valB), "ja")
    : String(valB).localeCompare(String(valA), "ja");
};

/* -----------------------------
   フィルタ
----------------------------- */
const filterName = ref(route.query.name || "");
const filterGrade = ref(route.query.grade || "");

// フィルタ適用
const filteredMembers = computed(() => {
  return activeMembers.value.filter((m) => {
    const gradeMatch =
      filterGrade.value === "" || m.grade === Number(filterGrade.value);

    // 大文字小文字を無視する場合はこちらを使用可能
    const nameMatch =
      filterName.value === "" ||
      m.name.toLowerCase().includes(filterName.value.toLowerCase());

    return gradeMatch && nameMatch;
  });
});

/* -----------------------------
   ソート情報
----------------------------- */
const sortKey = ref(route.query.sort || "grade");
const sortOrder = ref(route.query.order || "asc");

const toggleOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};

const sortedMembers = computed(() =>
  [...filteredMembers.value].sort((a, b) =>
    compareValues(a, b, sortKey.value, sortOrder.value),
  ),
);

const { currentPage, pageSize, totalPages, paginatedData } =
  usePagination(sortedMembers);

pageSize.value = Number(route.query.pageSize) || 10;

/* -----------------------------
   フィルタ・ソート・ページリセット
----------------------------- */
const resetFilters = () => {
  sortKey.value = "grade";
  sortOrder.value = "asc";
  filterName.value = "";
  filterGrade.value = "";
  currentPage.value = 1;
};
/* -----------------------------
   URL更新
----------------------------- */
watch([filterName, filterGrade, sortKey, sortOrder, pageSize], () => {
  currentPage.value = 1;
  router.replace({
    query: {
      name: filterName.value || undefined,
      grade: filterGrade.value || undefined,
      sort: sortKey.value,
      order: sortOrder.value,
      pageSize: pageSize.value !== 10 ? pageSize.value : undefined,
    },
  });
});

/* -----------------------------
   リセットボタン無効判定
----------------------------- */
const isResetDisabled = computed(() => {
  return (
    !filterName.value &&
    !filterGrade.value &&
    sortKey.value === "grade" &&
    sortOrder.value === "asc"
  );
});
</script>
