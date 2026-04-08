import { computed, toValue, type Ref } from "vue";
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";
import type { Measurement } from "@/services/measurementService";

type MaybeRef<T> = T | Ref<T>;

// ランキング1行分の型
export type RankingItem = {
  rank: number;
  user_id: number;
  name: string;
  grade: number | string | null;
  value: number;
};

export function useRankingData(measurements: MaybeRef<Measurement[]>) {
  /**
   * ref / computed / 生配列 すべて対応
   */
  const source = computed(() => toValue(measurements) ?? []);

  /**
   * 最新計測日の抽出
   */
  const latestMeasurements = computed(() => {
    if (!source.value.length) return [];

    const dates = source.value.map((m) => m.measurement_date);
    const latestDate = [...dates].sort().pop();

    return source.value.filter((m) => m.measurement_date === latestDate);
  });

  /**
   * 順位データ生成
   */
  const getRanking = (fieldKey: keyof Measurement): RankingItem[] => {
    if (!fieldKey) return [];

    const field = MEASUREMENT_FIELDS.find((f) => f.key === fieldKey);
    if (!field) return [];

    // 値があるデータのみ抽出
    const filtered = latestMeasurements.value
      .filter((m) => m[fieldKey] != null)
      .map((m) => ({
        user_id: m.user_id,
        name: m.name,
        grade: m.grade,
        value: m[fieldKey] as number, // ← Measurementのindexアクセス対策
      }));

    // ソート（lowerIsBetter対応）
    const sorted = filtered.sort((a, b) => {
      if (field.lowerIsBetter) {
        return a.value - b.value;
      } else {
        return b.value - a.value;
      }
    });

    // 順位付け（同率対応）
    let currentRank = 1;

    return sorted.map((item, index) => {
      if (index > 0 && item.value !== sorted[index - 1].value) {
        currentRank = index + 1;
      }

      return {
        rank: currentRank,
        user_id: item.user_id,
        name: item.name,
        grade: item.grade,
        value: item.value,
      };
    });
  };

  return {
    latestMeasurements,
    getRanking,
  };
}