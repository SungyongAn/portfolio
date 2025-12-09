<template>
  <div
    v-if="currentUser"
    class="user-info bg-white shadow-sm py-3 px-4 mb-3 position-sticky top-0 z-3"
  >
    <!-- 3列レイアウト -->
    <div class="d-flex justify-content-between align-items-center">
      <!-- 左側:ユーザー情報 -->
      <div class="d-flex align-items-center gap-2">
        <!-- バッジ（教師の種別に応じて表示） -->
        <span v-if="isTeacher()" class="badge bg-primary">
          {{ getTeacherBadgeText() }}
        </span>
        <span v-if="isSchoolNurse()" class="badge bg-success">看護教諭</span>
        <span v-if="isAdmin()" class="badge bg-warning text-dark">管理者</span>

        <!-- 氏名 -->
        <span class="fw-bold"
          >{{ currentUser.lastName }} {{ currentUser.firstName }}</span
        >

        <!-- 学年・組（管理者・看護教諭以外） -->
        <small class="text-muted" v-if="!isAdmin() && !isSchoolNurse()">
          {{ currentUser.grade ? currentUser.grade + "年" : "" }}
          {{ currentUser.className ? currentUser.className + "組" : "" }}
        </small>
      </div>

      <!-- 中央：戻るボタン + 画面タイトル -->
      <div v-if="pageTitle" class="d-flex align-items-center gap-3">
        <!-- 戻るボタン -->
        <button
          v-if="showBackButton"
          class="btn btn-outline-secondary btn-sm"
          @click="handleBack"
        >
          <i class="fas fa-arrow-left me-1"></i>戻る
        </button>

        <!-- タイトル -->
        <h4 class="mb-0">
          <i v-if="pageIcon" :class="pageIcon + ' me-2'"></i>
          {{ pageTitle }}
        </h4>
      </div>

      <!-- 右側：ログアウトボタン -->
      <div>
        <button
          class="btn btn-outline-danger btn-sm"
          @click.prevent="handleLogout"
        >
          <i class="fas fa-sign-out-alt me-1"></i>ログアウト
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "UserHeader",
  props: ["currentUser", "pageTitle", "pageIcon", "showBackButton"],
  emits: ["logout", "back"],
  methods: {
    handleLogout() {
      this.$emit("logout");
    },
    handleBack() {
      this.$emit("back");
    },
    isStudent() {
      return this.currentUser?.role === "student";
    },
    isTeacher() {
      return this.currentUser?.role === "teacher";
    },
    isSchoolNurse() {
      return this.currentUser?.role === "school_nurse";
    },
    isAdmin() {
      return this.currentUser?.role === "admin";
    },

    // 教師の種別チェック
    isGradeLeader() {
      return this.currentUser?.isGradeLeader;
    },
    isHomeroomTeacher() {
      return this.currentUser?.isHomeroomTeacher;
    },
    isAssistantTeacher() {
      return this.currentUser?.isAssistantTeacher;
    },
    isSubjectTeacher() {
      return this.currentUser?.isSubjectTeacher;
    },

    // バッジテキスト取得
    getTeacherBadgeText() {
      if (this.isGradeLeader()) return "学年主任";
      if (this.isHomeroomTeacher()) return "担任";
      if (this.isAssistantTeacher()) return "副担任";
      if (this.isSubjectTeacher()) return "教科担当";
      return "教師";
    },
  },
};
</script>
