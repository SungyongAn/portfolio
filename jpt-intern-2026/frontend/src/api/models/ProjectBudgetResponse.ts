/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type ProjectBudgetResponse = {
    id: number;
    project_id: number;
    budget_amount: number;
    unit_price?: (number | null);
    planned_months?: (number | null);
    actual_amount: number;
    consumption_rate?: number;
    created_at: string;
    updated_at: string;
};

