import { computed, toValue } from "vue";

export function useTrendData(measurements) {
  const source = computed(() => toValue(measurements) ?? []);

  // 部員一覧（name修正）
  const players = computed(() => {
    const map = new Map();
    source.value.forEach((m) => {
      if (!map.has(m.user_id)) {
        map.set(m.user_id, {
          id: m.user_id,
          name: m.name, // ← 修正①
        });
      }
    });
    return Array.from(map.values());
  });

  // 日付ごとにグループ化（measurement_date修正）
  const groupByDate = (data) => {
    const map = new Map();
    data.forEach((m) => {
      const date = m.measurement_date; // ← 修正②
      if (!map.has(date)) map.set(date, []);
      map.get(date).push(m);
    });
    return map;
  };

  // メイン：シリーズ生成
  const getTrendSeries = ({ fieldKey, userId = null }) => {
    let filtered = source.value;

    // 個人フィルタ
    if (userId) {
      filtered = filtered.filter((m) => m.user_id === userId);
    }

    const grouped = groupByDate(filtered);

    const labels = [];
    const data = [];

    // 日付順にソート（修正③）
    const sorted = [...grouped.entries()].sort(([a], [b]) => (a > b ? 1 : -1));

    sorted.forEach(([date, items]) => {
      labels.push(date);

      if (userId) {
        // 個人
        data.push(items[0][fieldKey]);
      } else {
        // チーム平均
        const avg =
          items.reduce((sum, m) => sum + (m[fieldKey] ?? 0), 0) / items.length;
        data.push(avg);
      }
    });

    return {
      labels,
      series: [
        {
          name: userId ? "個人" : "チーム平均",
          data,
        },
      ],
    };
  };

  return {
    players,
    getTrendSeries,
  };
}
