import { computed, toValue } from "vue";
import { MEASUREMENT_FIELDS } from "@/constants/measurementFields";

export function useRadarData(measurements) {
  // ref / computed 両対応
  const source = computed(() => toValue(measurements) || []);

  // ■ 最新計測日の抽出
  const latestMeasurements = computed(() => {
    const list = source.value;
    if (!list.length) return [];

    const latestDate = list
      .map((m) => m.measurement_date)
      .sort()
      .slice(-1)[0];

    return list.filter((m) => m.measurement_date === latestDate);
  });

  // ■ 部員一覧（全期間）
  const players = computed(() => {
    const map = new Map();

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

  // ■ min / max計算（最新データベース）
  const getMinMaxMap = () => {
    const result = {};

    MEASUREMENT_FIELDS.forEach((field) => {
      const values = latestMeasurements.value
        .map((m) => m[field.key])
        .filter((v) => v != null);

      const min = Math.min(...values);
      const max = Math.max(...values);

      result[field.key] = { min, max };
    });

    return result;
  };

  // ■ 正規化
  const normalize = (value, min, max) => {
    if (value == null) return 0;
    if (max === min) return 50; // 全員同じ値対策

    return ((value - min) / (max - min)) * 100;
  };

  // ■ 個人 or 複数選手のレーダーデータ
  const getRadarSeries = (playerIds = []) => {
    const minMaxMap = getMinMaxMap();

    return playerIds.map((id) => {
      const playerData = latestMeasurements.value.find((m) => m.user_id === id);

      const data = MEASUREMENT_FIELDS.map((field) => {
        const { min, max } = minMaxMap[field.key];

        let normalized = normalize(playerData?.[field.key], min, max);

        // ★ 追加（重要）
        if (field.lowerIsBetter) {
          normalized = 100 - normalized;
        }

        return normalized;
      });

      return {
        name: players.value.find((p) => p.id === id)?.name || "不明",
        value: data,
      };
    });
  };

  // ■ チーム平均
  const getTeamAvgSeries = () => {
    const minMaxMap = getMinMaxMap();

    const data = MEASUREMENT_FIELDS.map((field) => {
      const values = latestMeasurements.value
        .map((m) => m[field.key])
        .filter((v) => v != null);

      if (!values.length) return 0;

      const avg = values.reduce((sum, v) => sum + v, 0) / values.length;

      const { min, max } = minMaxMap[field.key];

      let normalized = normalize(avg, min, max);

      // ★ 追加（重要）
      if (field.lowerIsBetter) {
        normalized = 100 - normalized;
      }

      return normalized;
    });

    return [
      {
        name: "チーム平均",
        value: data,
      },
    ];
  };

  return {
    players,
    latestMeasurements,
    getRadarSeries,
    getTeamAvgSeries,
  };
}
