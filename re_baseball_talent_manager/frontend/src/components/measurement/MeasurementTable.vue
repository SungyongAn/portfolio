<template>
  <div class="table-responsive">
    <table class="table table-hover align-middle text-center">
      <thead class="table-light">
        <tr>
          <th v-if="isStaff" class="text-nowrap">部員名</th>
          <th v-if="isStaff" class="text-nowrap">学年</th>
          <th class="text-nowrap">計測年月</th>

          <!-- ✅ ここ1回だけ -->
          <th
            v-for="field in MEASUREMENT_FIELDS"
            :key="field.key"
            class="text-nowrap"
          >
            {{ field.label }} ({{ field.unit }})
          </th>

          <th v-if="showActions" class="text-nowrap">操作</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="m in measurements" :key="m.measurement_id">
          <td v-if="isStaff">{{ m.name }}</td>
          <td v-if="isStaff">{{ m.grade }}年</td>
          <td>{{ m.measurement_date.slice(0, 7) }}</td>

          <!-- ✅ tbodyも同じ構造 -->
          <td
            v-for="field in MEASUREMENT_FIELDS"
            :key="`${m.measurement_id}-${field.key}`"
          >
            {{ m[field.key] ?? "-" }} {{ field.unit }}
          </td>

          <td v-if="showActions">
            <div class="d-flex flex-wrap gap-2 justify-content-center">
              <button
                @click="$emit('approve', m.measurement_id)"
                class="btn btn-primary btn-sm"
                :disabled="submittingId === m.measurement_id"
              >
                承認
              </button>

              <button
                @click="$emit('reject', m.measurement_id)"
                class="btn btn-danger btn-sm"
                :disabled="submittingId === m.measurement_id"
              >
                否認
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";
import type { Measurement } from "@/services/measurement";

/* -----------------------------
   Props（省略形）
----------------------------- */

defineProps<{
  measurements: Measurement[];
  isStaff: boolean;
  showActions: boolean;
  submittingId?: number; // optional
}>();

/* -----------------------------
   Emits
----------------------------- */

const emit = defineEmits<{
  (e: "approve", measurementId: number): void;
  (e: "reject", measurementId: number): void;
}>();
</script>