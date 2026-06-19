/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DevelopmentMethod } from './DevelopmentMethod';
export type ProjectCreate = {
    name: string;
    description?: (string | null);
    budget_amount?: (number | null);
    planned_months?: (number | null);
    start_date?: (string | null);
    end_date?: (string | null);
    development_method?: (DevelopmentMethod | null);
};

