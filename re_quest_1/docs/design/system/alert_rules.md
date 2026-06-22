# alert_rules.md

# アラート判定設計

## 1. 概要

本ドキュメントは、`re_quest1` におけるアラート判定ルールを定義する。

本機能の目的は、案件の遅延や予算超過リスクを早期に発見し、ダッシュボード上で可視化することである。

第1段階では、既存 `quest_1` で実装した判定ロジックを維持する。

---

# 2. アラートレベル

アラートレベルは2段階とする。

| レベル  | 説明 |
| ------- | ---- |
| warning | 注意 |
| danger  | 危険 |

---

# 3. 判定対象

以下の指標を利用する。

| 指標             | 内容                       |
| ---------------- | -------------------------- |
| Progress         | 案件進捗率                 |
| Elapsed Rate     | 経過率                     |
| Consumption Rate | 予算消化率                 |
| SPI              | Schedule Performance Index |
| CPI              | Cost Performance Index     |
| Overdue Tasks    | 期限超過タスク数           |

---

# 4. 経過率

## 計算式

```text
経過率 = 経過日数 ÷ 全体期間 × 100
```

---

## 例

```text
開始日: 2026/05/01
終了日: 2026/05/31
今日: 2026/05/16

経過率 = 50%
```

---

# 5. 予算消化率

## 計算式

```text
消化率 = 実績合計 ÷ 予算額 × 100
```

---

## 実績合計

```text
実績工数費
＋
経費
```

---

# 6. SPI

## Schedule Performance Index

スケジュール健全性指標。

---

## 計算式

```text
SPI = Progress ÷ ElapsedRate
```

---

## 例

```text
進捗率 40%
経過率 50%

SPI = 0.80
```

---

## 判定

| SPI    | 状態     |
| ------ | -------- |
| >= 1.0 | 正常     |
| < 1.0  | 遅延傾向 |

---

# 7. CPI

## Cost Performance Index

コスト健全性指標。

---

## 計算式

```text
CPI = Progress ÷ ConsumptionRate
```

---

## 例

```text
進捗率 40%
消化率 60%

CPI = 0.67
```

---

## 判定

| CPI    | 状態           |
| ------ | -------------- |
| >= 1.0 | 正常           |
| < 1.0  | コスト超過傾向 |

---

# 8. Progress vs Elapsed

進捗率と経過率の差を判定する。

---

## Warning

```text
進捗率 - 経過率 <= -10%
```

---

## Danger

```text
進捗率 - 経過率 <= -20%
```

---

# 9. Progress vs Consumption

進捗率と予算消化率の差を判定する。

---

## Warning

```text
進捗率 - 消化率 <= -15%
```

---

## Danger

```text
進捗率 - 消化率 <= -25%
```

---

# 10. 期限超過タスク

期限超過タスク数を判定する。

---

## Warning

```text
期限超過タスク >= 1件
```

---

## Danger

```text
期限超過タスク >= 2件
```

---

# 11. 最終判定

複数条件に該当する場合は最も高いレベルを採用する。

---

## 優先順位

```text
danger
 ↓

warning
 ↓

normal
```

---

# 12. ダッシュボード表示

アラート判定結果は以下で利用する。

---

## Applicant Dashboard

- 自案件リスク表示

---

## Department Dashboard

- 部門リスク案件表示

---

## HQ Dashboard

- 全社リスク案件表示

---

## Alert Panel

- warning案件一覧
- danger案件一覧

---

# 13. レスポンス例

```json
{
  "project_id": 1,
  "project_name": "案件A",
  "alert_level": "danger",
  "spi": 0.75,
  "cpi": 0.68,
  "overdue_task_count": 3
}
```

---

# 14. 実装方針

ASP.NET Core版では、AlertServiceを利用する。

---

## 責務

- KPI計算
- SPI計算
- CPI計算
- リスク判定
- ダッシュボード用集計

---

## 想定クラス

```text
AlertService
DashboardService
```

---

# 15. 第1段階方針

既存PoCの判定ルールを維持する。

変更しない内容

- SPI計算
- CPI計算
- Warning基準
- Danger基準
- ダッシュボード連携

---

# 16. 今後の改善候補

移植完了後に検討する。

- アラート閾値設定画面
- 部門別閾値
- 案件種別別閾値
- リスク予測AI
- トレンド分析
- KPI履歴表示

---

# 17. まとめ

本システムでは、

```text
SPI
CPI
進捗率
経過率
予算消化率
期限超過タスク
```

を利用して案件リスクを判定する。

第1段階では既存PoCの判定ロジックを維持し、React + ASP.NET Core版へ移植する。
