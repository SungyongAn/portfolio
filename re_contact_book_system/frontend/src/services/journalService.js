import api from './api'

// 連絡帳を提出する（生徒）
export function submitJournal(payload) {
  return api.post('/api/journals/', payload)
}


// 生徒：過去の連絡帳一覧
export function getMyJournalHistory(params = {}) {
  return api.get('/api/journals/history', { params })
}

// 生徒：今日の連絡帳（未提出なら 404）
export function getTodayJournal() {
  return api.get('/api/journals/today')
}

// 生徒：推奨記入日取得
export function getSuggestedDate() {
  return api.get('/api/journals/suggested-date')
}

// 連絡帳詳細（生徒・教師共通）
export function getJournalById(journalId) {
  return api.get(`/api/journals/${journalId}`)
}

// 教師：既読にする
export function markAsRead(journalId) {
  return api.put(`/api/journals/${journalId}/read`)
}
