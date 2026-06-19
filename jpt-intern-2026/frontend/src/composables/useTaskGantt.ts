import { computed, ref } from "vue";
import type { TaskResponse } from "@/api/models/TaskResponse";

export type GanttViewMode = "day" | "week" | "month";

export const viewModeOptions = [
  { label: "日", value: "day" },
  { label: "週", value: "week" },
  { label: "月", value: "month" },
] as const;

const toDate = (value?: string | null): Date | null => {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? null : date;
};

const formatDateKey = (date: Date): string => {
  return date.toISOString().slice(0, 10);
};

const addDays = (date: Date, days: number): Date => {
  const next = new Date(date);
  next.setDate(next.getDate() + days);
  return next;
};

const diffDays = (from: Date, to: Date): number => {
  const fromDate = new Date(formatDateKey(from));
  const toDateValue = new Date(formatDateKey(to));
  return Math.floor(
    (toDateValue.getTime() - fromDate.getTime()) / (1000 * 60 * 60 * 24),
  );
};

export const useTaskGantt = (tasksRef: { value: TaskResponse[] }) => {
  const selectedAssignee = ref("");
  const viewMode = ref<GanttViewMode>("day");

  const filteredTasks = computed(() => {
    if (!selectedAssignee.value) return tasksRef.value;

    return tasksRef.value.filter((task) => {
      const assigneeName = task.assignee_name || "未割当";
      return assigneeName === selectedAssignee.value;
    });
  });

  const assigneeOptions = computed(() => {
    return Array.from(
      new Set(tasksRef.value.map((task) => task.assignee_name || "未割当")),
    );
  });

  const ganttRange = computed(() => {
    const dates = filteredTasks.value
      .flatMap((task) => [toDate(task.start_date), toDate(task.due_date)])
      .filter((date): date is Date => date !== null);

    if (dates.length === 0) {
      const today = new Date();
      return {
        start: addDays(today, -7),
        end: addDays(today, 30),
      };
    }

    const min = new Date(Math.min(...dates.map((date) => date.getTime())));
    const max = new Date(Math.max(...dates.map((date) => date.getTime())));

    return {
      start: addDays(min, -3),
      end: addDays(max, 7),
    };
  });

  const dayWidth = computed(() => {
    switch (viewMode.value) {
      case "week":
        return 12;
      case "month":
        return 5;
      case "day":
      default:
        return 34;
    }
  });

  const timelineDays = computed(() => {
    const days: Date[] = [];
    const totalDays = diffDays(ganttRange.value.start, ganttRange.value.end);

    for (let i = 0; i <= totalDays; i += 1) {
      days.push(addDays(ganttRange.value.start, i));
    }

    return days;
  });

  const timelineWidth = computed(() => {
    return timelineDays.value.length * dayWidth.value;
  });

  const visibleTimelineDays = computed(() => {
    if (viewMode.value === "day") return timelineDays.value;

    if (viewMode.value === "week") {
      return timelineDays.value.filter((_, index) => index % 7 === 0);
    }

    return timelineDays.value.filter((date, index) => {
      return index === 0 || date.getDate() === 1;
    });
  });

  const getDateLabel = (date: Date): string => {
    if (viewMode.value === "month") {
      return `${date.getMonth() + 1}月`;
    }

    if (viewMode.value === "week") {
      return `${date.getMonth() + 1}/${date.getDate()}`;
    }

    return `${date.getDate()}`;
  };

  const getDateLeft = (date: Date): number => {
    return diffDays(ganttRange.value.start, date) * dayWidth.value;
  };

  const getTaskBarStyle = (task: TaskResponse) => {
    const startDate = toDate(task.start_date);
    const dueDate = toDate(task.due_date);

    if (!startDate || !dueDate) return null;

    const offset = diffDays(ganttRange.value.start, startDate);
    const duration = Math.max(diffDays(startDate, dueDate) + 1, 1);

    return {
      left: `${offset * dayWidth.value}px`,
      width: `${duration * dayWidth.value}px`,
    };
  };

  const todayLineStyle = computed(() => {
    const today = new Date();

    if (today < ganttRange.value.start || today > ganttRange.value.end) {
      return null;
    }

    return {
      left: `${diffDays(ganttRange.value.start, today) * dayWidth.value}px`,
    };
  });

  return {
    selectedAssignee,
    viewMode,
    viewModeOptions,
    filteredTasks,
    assigneeOptions,
    timelineDays,
    visibleTimelineDays,
    timelineWidth,
    dayWidth,
    todayLineStyle,
    getDateLabel,
    getDateLeft,
    getTaskBarStyle,
  };
};
