/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExpenseType } from './ExpenseType';
export type ExpenseResponse = {
    id: number;
    project_id: number;
    expense_type: ExpenseType;
    amount: number;
    description?: (string | null);
    expense_date: string;
    created_at: string;
    updated_at: string;
};

