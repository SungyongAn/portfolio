import { ref, computed, watch, type Ref } from "vue";

export function usePagination<T>(data: Ref<T[]>) {
  const currentPage = ref(1);
  const pageSize = ref(10);

  const totalPages = computed(() =>
    Math.ceil(data.value.length / pageSize.value),
  );

  const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value;
    return data.value.slice(start, start + pageSize.value);
  });

  // ページ補正（これ重要）
  watch(totalPages, (newTotal) => {
    if (newTotal === 0) {
      currentPage.value = 1;
    } else if (currentPage.value > newTotal) {
      currentPage.value = newTotal;
    }
  });

  return {
    currentPage,
    pageSize,
    totalPages,
    paginatedData,
  };
}