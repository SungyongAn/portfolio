

<template>
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
        <tr v-for="member in members" :key="member.user_id">
          <td>{{ member.name }}</td>
          <td>{{ member.grade }}年</td>
          <td>
            <span class="badge bg-success">在籍中</span>
          </td>
          <td>
            <div class="d-flex gap-2">
              <button
                class="btn btn-sm btn-outline-warning"
                @click="emit('retire', member)"
              >
                引退
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                @click="emit('withdraw', member)"
              >
                退部
              </button>
            </div>
          </td>
        </tr>

        <tr v-if="members.length === 0">
          <td colspan="4" class="text-center text-muted">
            在籍中の部員はいません
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
/* -----------------------------
  型インポート
----------------------------- */
import type { User } from "@/services/userService"

/* -----------------------------
  Props
----------------------------- */
const props = defineProps<{
  members: User[]
}>()

/* -----------------------------
  Emits
----------------------------- */
const emit = defineEmits<{
  (e: "retire", user: User): void
  (e: "withdraw", user: User): void
}>()
</script>