// components/projects/gantt/useGanttTasks.ts

import { computed, type Ref } from "vue";

import type { TaskResponse } from "@/api/models/TaskResponse";

import { PHASE_ORDER } from "@/constants/task";

export function useGanttTasks(
  tasks: Ref<TaskResponse[]>,
  selectedPersons: Ref<Set<string>>,
) {
  // ── 担当者一覧 ───────────────────────────

  const allPersons = computed(() => {
    const names = tasks.value
      .map((t) => t.assignee_name)
      .filter((n): n is string => n !== null && n !== undefined);

    return [...new Set(names)];
  });

  // ── 工程順取得 ───────────────────────────

  const getPhaseOrder = (phaseName?: string | null) => {
    if (!phaseName) return 999;

    return PHASE_ORDER[phaseName] ?? 999;
  };

  // ── 表示対象タスク ───────────────────────

  const visibleTasks = computed(() => {
    const list = tasks.value.filter((t) => {
      if (selectedPersons.value.size === 0) {
        return true;
      }

      return selectedPersons.value.has(t.assignee_name ?? "");
    });

    return [...list].sort((a, b) => {
      // 工程順
      const pa = getPhaseOrder(a.phase_name);
      const pb = getPhaseOrder(b.phase_name);

      if (pa !== pb) {
        return pa - pb;
      }

      // 開始日順
      const sa = a.start_date ?? "";
      const sb = b.start_date ?? "";

      if (sa !== sb) {
        return sa.localeCompare(sb);
      }

      // 担当者順
      const ua = a.assignee_name ?? "";
      const ub = b.assignee_name ?? "";

      if (ua !== ub) {
        return ua.localeCompare(ub, "ja");
      }

      // タスク名順
      return a.name.localeCompare(b.name, "ja");
    });
  });

  // ── フィルター操作 ─────────────────────

  function togglePersonFilter(name: string) {
    const next = new Set(selectedPersons.value);

    if (next.has(name)) {
      next.delete(name);
    } else {
      next.add(name);
    }

    selectedPersons.value = next;
  }

  function resetFilters() {
    selectedPersons.value = new Set();
  }

  return {
    allPersons,
    visibleTasks,
    togglePersonFilter,
    resetFilters,
  };
}
