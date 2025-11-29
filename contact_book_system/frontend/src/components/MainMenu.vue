<template>
    <div class="d-flex justify-content-center align-items-center vh-100">
      <div class="p-4 bg-white shadow rounded" style="max-width:600px; width:100%;">

        <!-- 生徒用メニュー -->
        <template v-if="isStudent()">
          <ul class="nav flex-column">
            <li class="nav-item mb-2">
              <button class="btn btn-outline-primary w-100" @click.prevent="navigate('entry-form')">
                <i class="fas fa-calendar-day me-2"></i>連絡帳の提出
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-primary w-100" @click.prevent="navigate('past-renrakucho-search')">
                <i class="fas fa-history me-2"></i>過去の連絡帳（閲覧のみ）
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-success w-100" @click.prevent="navigate('chat-room-list')">
                <i class="fas fa-comments me-2"></i>報連相部屋(仮)
              </button>
            </li>
          </ul>
        </template>

        <!-- 学年主任用メニュー -->
        <template v-if="isGradeLeader()">
          <ul class="nav flex-column mb-3">
            <li class="nav-item mb-2">
              <button class="btn btn-outline-secondary w-100" @click.prevent="navigate('submission-status')">
                <i class="fas fa-file-alt me-2"></i>連絡帳提出状況
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-secondary w-100" @click.prevent="navigate('class-entry-renrakucho')">
                <i class="fas fa-file-alt me-2"></i>未確認の連絡帳
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-secondary w-100" @click.prevent="navigate('class-past-renrakucho')">
                <i class="fas fa-folder-open me-2"></i>過去の連絡帳
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-success w-100" @click.prevent="navigate('chat-room-list')">
                <i class="fas fa-comments me-2"></i>報連相部屋(仮)
              </button>
            </li>
          </ul>
        </template>

        <!-- 担任・副担任用メニュー -->
        <template v-if="isHomeroomTeacher() || isAssistantTeacher()">
          <ul class="nav flex-column mb-3">
            <li class="nav-item mb-2">
              <button class="btn btn-outline-secondary w-100" @click.prevent="navigate('submission-status')">
                <i class="fas fa-file-alt me-2"></i>連絡帳提出状況
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-secondary w-100" @click.prevent="navigate('class-entry-renrakucho')">
                <i class="fas fa-file-alt me-2"></i>未確認の連絡帳
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-secondary w-100" @click.prevent="navigate('class-past-renrakucho')">
                <i class="fas fa-folder-open me-2"></i>過去の連絡帳
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-success w-100" @click.prevent="navigate('chat-room-list')">
                <i class="fas fa-comments me-2"></i>報連相部屋(仮)
              </button>
            </li>
          </ul>
        </template>

        <!-- 教科担当用メニュー -->
        <template v-if="isSubjectTeacher()">
          <ul class="nav flex-column mb-3">
            <li class="nav-item mb-2">
              <button class="btn btn-outline-success w-100" @click.prevent="navigate('chat-room-list')">
                <i class="fas fa-comments me-2"></i>報連相部屋(仮)
              </button>
            </li>
          </ul>
        </template>

        <!-- 養護教諭用メニュー -->
        <template v-if="isSchoolNurse()">
          <ul class="nav flex-column mb-3">
            <li class="nav-item mb-2">
              <button class="btn btn-outline-success w-100" @click.prevent="navigate('chat-room-list')">
                <i class="fas fa-comments me-2"></i>報連相部屋(仮)
              </button>
            </li>
            <li class="nav-item mb-2">
              <button class="btn btn-outline-success w-100" @click.prevent="navigate('school-nurse-dashboard')">
                <i class="fas fa-comments me-2"></i>生徒の状況確認(仮)
              </button>
            </li>
          </ul>
        </template>
      </div>
    </div>
</template>

<script>
export default {
  props: ['currentUser', 'isLoggedIn'],
  emits: ['logout', 'navigate'],
  methods: {
    handleLogout() {
      this.$emit('logout');
    },
    navigate(componentName) {
      this.$emit('navigate', componentName);
    },
    isStudent() {
      return this.currentUser && this.currentUser.role === 'student';
    },
    isTeacher() {
      return this.currentUser && this.currentUser.role === 'teacher';
    },
    isSchoolNurse() {
      return this.currentUser && this.currentUser.role === 'school_nurse';
    },
    isAdmin() {
      return this.currentUser && this.currentUser.role === 'admin';
    },

    // 教師の種別チェック
    isGradeLeader() {
      return this.currentUser && this.currentUser.teacherRole === 'grade_leader';
    },
    isHomeroomTeacher() {
      return this.currentUser && this.currentUser.teacherRole === 'homeroom';
    },
    isAssistantTeacher() {
      return this.currentUser && this.currentUser.teacherRole === 'assistant_homeroom';
    },
    isSubjectTeacher() {
      return this.currentUser && this.currentUser.teacherRole === 'subject_teacher';
    }
  }
};
</script>
