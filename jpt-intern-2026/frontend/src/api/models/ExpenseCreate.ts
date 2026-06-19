/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ExpenseType } from './ExpenseType';
export type ExpenseCreate = {
    expense_type: ExpenseType;
    amount: number;
    description?: (string | null);
    expense_date: string;
};

