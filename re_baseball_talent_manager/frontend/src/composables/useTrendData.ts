import { computed, toValue, type Ref } from "vue";
import type { Measurement } from "@/services/measurementService";

type MaybeRef<T> = T | Ref<T>;

type Player = {
  id: number;
  name: string;
};

// groupByDateの戻り値
type GroupedByDate = Map<string, Measurement[]>;

// getTrendSeriesの引数
type TrendParams = {
  fieldKey: keyof Measurement;
  userId?: number | null;
};

// getTrendSeriesの戻り値
type TrendSeries = {
  labels: string[];
  series: {
    name: string;
    data: number[];
  }[];
};

export function useTrendData(measurements: MaybeRef<Measurement[]>) {
  const source = computed(() => toValue(measurements) ?? []);

  // 部員一覧
  const players = computed<Player[]>(() => {
    const map = new Map<number, Player>();

    source.value.forEach((m) => {
      if (!map.has(m.user_id)) {
        map.set(m.user_id, {
          id: m.user_id,
          name: m.name,
        });
      }
    });

    return Array.from(map.values());
  });

  // 日付ごとにグループ化
  const groupByDate = (data: Measurement[]): GroupedByDate => {
    const map: GroupedByDate = new Map();

    data.forEach((m) => {
      const date = m.measurement_date;
      if (!map.has(date)) map.set(date, []);
      map.get(date)!.push(m);
    });

    return map;
  };

  // メイン：シリーズ生成
  const getTrendSeries = ({ fieldKey, userId = null }: TrendParams): TrendSeries => {
    let filtered = source.value;

    // 個人フィルタ
    if (userId) {
      filtered = filtered.filter((m) => m.user_id === userId);
    }

    const grouped = groupByDate(filtered);

    const labels: string[] = [];
    const data: number[] = [];

    // 日付順ソート
    const sorted = [...grouped.entries()].sort(([a], [b]) => (a > b ? 1 : -1));

    sorted.forEach(([date, items]) => {
      labels.push(date);

      if (userId) {
        // 個人
        const value = items[0]?.[fieldKey];
        data.push(typeof value === "number" ? value : 0);
      } else {
        // チーム平均
        const values = items
          .map((m) => m[fieldKey])
          .filter((v): v is number => v != null);

        const avg = values.length
          ? values.reduce((sum, v) => sum + v, 0) / values.length
          : 0;

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