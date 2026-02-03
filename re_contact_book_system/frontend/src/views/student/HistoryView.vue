<template>
  <div class="container mt-5">
    <h1 class="mb-4">連絡帳 提出履歴</h1>

    <table class="table table-striped">
      <thead>
        <tr>
          <th>対象日</th>
          <th>体調</th>
          <th>気分</th>
          <th>既読</th>
          <th>提出日</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="journal in journals" :key="journal.id">
          <td>{{ journal.entry_date }}</td>
          <td>{{ journal.physical_condition }}</td>
          <td>{{ journal.mental_condition }}</td>
          <td>
            <span
              class="badge"
              :class="journal.is_read ? 'bg-success' : 'bg-secondary'"
            >
              {{ journal.is_read ? '既読' : '未読' }}
            </span>
          </td>
          <td>{{ journal.submission_date }}</td>
        </tr>
      </tbody>
    </table>

    <router-link
      to="/student/dashboard"
      class="btn btn-secondary mt-3"
    >
      戻る
    </router-link>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const journals = ref([])

async function loadHistory() {
  const res = await api.get('/api/journals/history', {
    params: {
      limit: 50,
      offset: 0
    }
  })
  journals.value = res.data
}

onMounted(loadHistory)
</script>
