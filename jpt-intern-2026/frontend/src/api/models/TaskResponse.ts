/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TaskStatus } from './TaskStatus';
export type TaskResponse = {
    id: number;
    project_id: number;
    name: string;
    phase_name?: (string | null);
    description?: (string | null);
    assignee_id?: (number | null);
    assignee_name?: (string | null);
    status: TaskStatus;
    progress: number;
    start_date?: (string | null);
    due_date?: (string | null);
    created_at: string;
    updated_at: string;
};

