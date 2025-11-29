<template>
    <div class="d-flex justify-content-center px-2">
  <div class="d-flex" style="max-width: 900px; width: 100%;">

    <!-- 左側：縦列サマリー -->
<div class="d-flex flex-column me-3" style="width: 150px;">
  <div 
    class="p-2 mb-2 rounded border bg-white text-center cursor-pointer"
    :class="displayMode === 'all' ? 'border-primary text-primary' : ''"
    @click="setDisplayMode('all')"
    style="cursor: pointer;">
    <p class="mb-1 fw-bold">クラス全体</p>
    <h5 class="mb-0">{{ submissionData?.total_students || 0 }}名</h5>
  </div>
  <div 
    class="p-2 mb-2 rounded border bg-white text-center cursor-pointer"
    :class="displayMode === 'submitted' ? 'border-success text-success' : ''"
    @click="setDisplayMode('submitted')"
    style="cursor: pointer;">
    <p class="mb-1 fw-bold">提出済み</p>
    <h5 class="mb-0">{{ submissionData?.submitted_count || 0 }}名</h5>
  </div>
  <div 
    class="p-2 mb-2 rounded border bg-white text-center cursor-pointer"
    :class="displayMode === 'not_submitted' ? 'border-danger text-danger' : ''"
    @click="setDisplayMode('not_submitted')"
    style="cursor: pointer;">
    <p class="mb-1 fw-bold">未提出</p>
    <h5 class="mb-0">{{ submissionData?.not_submitted_count || 0 }}名</h5>
  </div>
</div>


    <!-- 右側：カード本体 -->
    <div class="card p-4 w-100">

      <!-- エラー表示 -->
      <div v-if="errorMessage" class="alert alert-danger text-center">
        <i class="fas fa-exclamation-circle me-2"></i>{{ errorMessage }}
      </div>

      <!-- 日付選択 -->
      <div class="mb-4">
        <div class="d-flex align-items-center">
          <label class="form-label mb-0 me-2" style="font-size: 1rem;">対象日</label>
          <input 
            type="date" 
            class="form-control"
            style="width: 150px;"
            v-model="targetDate"
            :max="todayDate"
            :disabled="isLoading">

          <button 
            class="btn btn-outline-secondary mx-2"
            @click="setToday"
            :disabled="isLoading">
            <i class="fas fa-calendar-day me-2"></i>今日
          </button>
          <button 
            class="btn btn-primary mx-2"
            @click="checkSubmissionStatus"
            :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-search me-2"></i>
            {{ isLoading ? '確認中...' : '提出状況を確認' }}
          </button>
        </div>
      </div>

      <!-- 生徒リスト -->
      <div v-if="submissionData && displayStudents.length > 0">
        <div class="d-flex flex-wrap justify-content-start">
          <div 
            v-for="(column, colIndex) in studentColumns" 
            :key="colIndex"
            class="me-4 mb-3"
            style="min-width: 200px;">
            <ul class="list-group">
              <li 
                v-for="student in column" 
                :key="student.student_id"
                class="list-group-item d-flex justify-content-between align-items-center">
                <span><i class="fas fa-user me-2"></i>{{ student.student_name }}</span>
                <span class="badge px-2 py-1" :class="getStatusBadge(student)" style="font-size: 0.9rem;">
                  {{ getStatusText(student) }}
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 該当なし -->
      <div v-if="submissionData && displayStudents.length === 0 && !isLoading" 
           class="alert alert-info text-center">
        <i class="fas fa-info-circle me-2"></i>該当する生徒がいません
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
import { API_BASE_URL } from '../../config'

export default {
  props: ['currentUser'],
  emits: ['new-entry', 'back', 'updateTitle'], 
  data() {
    const today = new Date();
    return {
      targetDate: today.toISOString().split('T')[0],
      submissionData: null,
      isLoading: false,
      errorMessage: '',
      displayMode: 'all' // 'all', 'submitted', 'not_submitted'
    };
  },
  computed: {
    todayDate() {
      return new Date().toISOString().split('T')[0];
    },
    displayStudents() {
      if (!this.submissionData) return [];

      // 各生徒に is_submitted フラグを付与して結合
      switch(this.displayMode) {
        case 'submitted':
          return (this.submissionData.submitted_students || []).map(s => ({
            ...s,
            is_submitted: true
          }));
        case 'not_submitted':
          return (this.submissionData.not_submitted_students || []).map(s => ({
            ...s,
            is_submitted: false
          }));
        case 'all':
        default:
          const submitted = (this.submissionData.submitted_students || []).map(s => ({
            ...s,
            is_submitted: true
          }));
          const notSubmitted = (this.submissionData.not_submitted_students || []).map(s => ({
            ...s,
            is_submitted: false
          }));
          return [...submitted, ...notSubmitted].sort((a, b) =>
            a.student_name.localeCompare(b.student_name, 'ja')
          );
      }
    },
    studentColumns() {
      const students = this.displayStudents;
      const chunkSize = 10;
      const columns = [];
      for (let i = 0; i < students.length; i += chunkSize) {
        columns.push(students.slice(i, i + chunkSize));
      }
      return columns;
    }
  },
  mounted() {
    // 初回データ取得
    this.checkSubmissionStatus();

    // ヘッダーにタイトルと戻るボタンを設定
    this.$emit('updateTitle', {
      title: '連絡帳の提出状況',
      icon: 'fas fa-folder-open',
      showBackButton: true
    });
  },
  beforeUnmount() {
    // コンポーネント離脱時にタイトルをクリア
    this.$emit('updateTitle', {
      title: '',
      icon: '',
      showBackButton: false
    });
  },
  methods: {
    async checkSubmissionStatus(event) {
      if (event) {
        event.preventDefault();
        event.stopPropagation();
      }

      if (!this.currentUser || this.currentUser.role !== 'teacher') {
        this.errorMessage = '教師のみ利用可能です';
        return;
      }

      this.isLoading = true;
      this.errorMessage = '';
      this.submissionData = null;
      this.displayMode = 'all'; // リセット

      const payload = {
        grade: Number(this.currentUser.grade),
        class_name: this.currentUser.className,
        target_date: this.targetDate
      };

      try {
        const response = await axios.post(
          `${API_BASE_URL}/renrakucho-management/submission-status`,
          payload
        );

        if (response.data.success) {
          this.submissionData = response.data.data;
        } else {
          this.errorMessage = response.data.message || '提出状況の取得に失敗しました';
        }
      } catch (error) {
        this.errorMessage = error.response?.data?.detail || 'サーバーとの通信に失敗しました';
      } finally {
        this.isLoading = false;
      }
    },
    setToday() {
      this.targetDate = this.todayDate;
    },
    setDisplayMode(mode) {
      this.displayMode = mode;
    },

    // ✅ 方法②：バッジ色をモードに応じて変更
    getStatusBadge(student) {
      if (this.displayMode === 'submitted') {
        return 'bg-success';
      } else if (this.displayMode === 'not_submitted') {
        return 'bg-danger';
      } else {
        return student.is_submitted ? 'bg-success' : 'bg-danger';
      }
    },

    // ✅ 方法①：表示文言をモードに応じて変更
    getStatusText(student) {
      if (this.displayMode === 'submitted') {
        return '提出済み';
      } else if (this.displayMode === 'not_submitted') {
        return '未提出';
      } else {
        return student.is_submitted ? '提出済み' : '未提出';
      }
    }
  }
};
</script>
