/**
 * useProjectTable.ts
 * プロジェクトテーブル系コンポーネントで共通利用するロジック
 */
import { PROJECT_STATUS_LABEL, PROJECT_STATUS_TAG_TYPE } from "@/constants/project";
import type { ProjectStatus } from "@/api/models/ProjectStatus";

export function useProjectTable() {
  /** 日付文字列を YYYY-MM-DD 形式に整形 */
  const formatDate = (dateStr: string): string => {
    return dateStr.substring(0, 10);
  };

  /** 予算消化率に応じた el-progress の status を返す */
  const getConsumptionStatus = (
    rate: number | null,
  ): "exception" | "warning" | undefined => {
    if (rate === null) return undefined;
    if (rate >= 100) return "exception";
    if (rate >= 80) return "warning";
    return undefined;
  };

  /** 承認ステップの el-tag タイプを返す（申請者向け） */
  const getApprovalStepType = (
    status: ProjectStatus,
    step: "dept" | "hq" | "approved",
  ): string => {
    if (status === "REJECTED") return "danger";
    const passedStatuses = [
      "PENDING_HQ",
      "APPROVED",
      "IN_PROGRESS",
      "COMPLETED",
    ];
    const completedStatuses = ["APPROVED", "IN_PROGRESS", "COMPLETED"];
    if (step === "dept") {
      if (status === "PENDING_DEPT") return "warning";
      if (passedStatuses.includes(status)) return "success";
      return "info";
    }
    if (step === "hq") {
      if (status === "PENDING_HQ") return "warning";
      if (completedStatuses.includes(status)) return "success";
      return "info";
    }
    if (step === "approved") {
      if (completedStatuses.includes(status)) return "success";
      return "info";
    }
    return "info";
  };

  return {
    PROJECT_STATUS_LABEL,
    PROJECT_STATUS_TAG_TYPE,
    formatDate,
    getConsumptionStatus,
    getApprovalStepType,
  };
}
