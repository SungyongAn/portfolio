<template>
  <div class="container mt-5">
    <h1 class="mb-4">連絡帳提出</h1>

    <!-- 提出済み -->
    <div v-if="alreadySubmitted" class="alert alert-info">
      本日の連絡帳はすでに提出済みです。
    </div>

    <!-- 未提出 -->
    <form v-else @submit.prevent="submitJournal">
      <!-- 対象日 -->
      <div class="mb-3">
        <label class="form-label">対象日</label>
        <input
          type="date"
          class="form-control"
          v-model="form.entry_date"
          readonly
        />
      </div>

      <!-- 体調 -->
      <div class="mb-3">
        <label class="form-label">体調</label>
        <select v-model="form.physical_condition" class="form-select" required>
          <option disabled value="">選択してください</option>
          <option>とても良い</option>
          <option>良い</option>
          <option>普通</option>
          <option>悪い</option>
        </select>
      </div>

      <!-- 気分 -->
      <div class="mb-3">
        <label class="form-label">気分</label>
        <select v-model="form.mental_condition" class="form-select" required>
          <option disabled value="">選択してください</option>
          <option>元気</option>
          <option>普通</option>
          <option>少し疲れた</option>
          <option>疲れた</option>
        </select>
      </div>

      <!-- 振り返り -->
      <div class="mb-3">
        <label class="form-label">今日の振り返り</label>
        <textarea
          v-model="form.reflection_text"
          class="form-control"
          rows="4"
          required
        />
      </div>

      <button class="btn btn-primary">提出</button>
      <router-link to="/student/dashboard" class="btn btn-secondary ms-2">
        戻る
      </router-link>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import router from '@/router'

const alreadySubmitted = ref(false)

const form = ref({
  entry_date: '',
  physical_condition: '',
  mental_condition: '',
  reflection_text: ''
})

// 前登校日取得（サーバーに任せるのが理想）
async function loadTodayStatus() {
  const res = await api.get('/api/journals/today')
  if (res.data) {
    alreadySubmitted.value = true
  } else {
    // 未提出 → entry_date を設定
    form.value.entry_date = res.headers['x-entry-date']
    // ↑ もしくは別APIで取得
  }
}

async function submitJournal() {
  await api.post('/api/journals', form.value)
  router.push('/student/dashboard')
}

onMounted(loadTodayStatus)
</script>
