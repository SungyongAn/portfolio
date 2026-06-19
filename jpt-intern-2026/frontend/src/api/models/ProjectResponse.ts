/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DevelopmentMethod } from './DevelopmentMethod';
import type { ProjectStatus } from './ProjectStatus';
export type ProjectResponse = {
    id: number;
    name: string;
    description?: (string | null);
    status: ProjectStatus;
    development_method?: (DevelopmentMethod | null);
    applicant_id: number;
    department_id: number;
    department_name?: (string | null);
    applicant_name?: (string | null);
    budget_amount?: (number | null);
    planned_months?: (number | null);
    start_date?: (string | null);
    end_date?: (string | null);
    reject_reason?: (string | null);
    progress?: number;
    alert_level?: (string | null);
    alert_reason?: (string | null);
    actual_amount?: (number | null);
    consumption_rate?: (number | null);
    created_at: string;
    updated_at: string;
};

