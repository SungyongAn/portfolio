import type { ExpenseType } from "@/api/models/ExpenseType";

export const EXPENSE_TYPE_LABEL: Record<ExpenseType, string> = {
  OUTSOURCING: "外注費",
  LICENSE: "ライセンス費",
  EQUIPMENT: "機材費",
  OTHER: "その他",
};
