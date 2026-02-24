import { defineStore } from 'pinia'
import * as journalService from '@/services/journalService'

export const useJournalStore = defineStore('journal', {
  state: () => ({
    journals: [],
    todaySubmitted: false,
    loading: false
  }),

  actions: {
    async fetchMyJournals() {
      this.loading = true
      try {
        const res = await journalService.getMyJournals()
        this.journals = res.data
      } finally {
        this.loading = false
      }
    },

    async submitJournal(payload) {
      await journalService.createJournal(payload)
      this.todaySubmitted = true
    },

    async checkToday() {
      const res = await journalService.checkTodaySubmission()
      this.todaySubmitted = !!res.data
    }
  }
})
