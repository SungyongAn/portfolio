/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TaskStatus } from './TaskStatus';
export type TaskCreate = {
    name: string;
    phase_name?: (string | null);
    description?: (string | null);
    assignee_id?: (number | null);
    status?: TaskStatus;
    progress?: number;
    start_date?: (string | null);
    due_date?: (string | null);
};

