/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ApprovalRequest } from '../models/ApprovalRequest';
import type { BudgetSummaryResponse } from '../models/BudgetSummaryResponse';
import type { DepartmentResponse } from '../models/DepartmentResponse';
import type { ExpenseCreate } from '../models/ExpenseCreate';
import type { ExpenseResponse } from '../models/ExpenseResponse';
import type { ExpenseUpdate } from '../models/ExpenseUpdate';
import type { LoginRequest } from '../models/LoginRequest';
import type { NotificationListResponse } from '../models/NotificationListResponse';
import type { NotificationResponse } from '../models/NotificationResponse';
import type { ProjectBudgetCreate } from '../models/ProjectBudgetCreate';
import type { ProjectBudgetResponse } from '../models/ProjectBudgetResponse';
import type { ProjectBudgetUpdate } from '../models/ProjectBudgetUpdate';
import type { ProjectCreate } from '../models/ProjectCreate';
import type { ProjectListResponse } from '../models/ProjectListResponse';
import type { ProjectResponse } from '../models/ProjectResponse';
import type { ProjectUpdate } from '../models/ProjectUpdate';
import type { RefreshRequest } from '../models/RefreshRequest';
import type { TaskCreate } from '../models/TaskCreate';
import type { TaskResponse } from '../models/TaskResponse';
import type { TaskUpdate } from '../models/TaskUpdate';
import type { TokenResponse } from '../models/TokenResponse';
import type { UserCreate } from '../models/UserCreate';
import type { UserResponse } from '../models/UserResponse';
import type { WorklogCreate } from '../models/WorklogCreate';
import type { WorklogResponse } from '../models/WorklogResponse';
import type { WorklogUpdate } from '../models/WorklogUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Service {
    /**
     * Login
     * ログイン
     * @param requestBody
     * @returns TokenResponse Successful Response
     * @throws ApiError
     */
    public static loginApiAuthLoginPost(
        requestBody: LoginRequest,
    ): CancelablePromise<TokenResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/login',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Refresh
     * アクセストークンのリフレッシュ
     * @param requestBody
     * @returns TokenResponse Successful Response
     * @throws ApiError
     */
    public static refreshApiAuthRefreshPost(
        requestBody: RefreshRequest,
    ): CancelablePromise<TokenResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/auth/refresh',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Users
     * ユーザー一覧取得（本部管理者のみ）
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static getUsersApiUsersGet(): CancelablePromise<Array<UserResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users',
        });
    }
    /**
     * Create User
     * ユーザー作成（本部管理者のみ）
     * @param requestBody
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static createUserApiUsersPost(
        requestBody: UserCreate,
    ): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/users',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Me
     * ログイン中のユーザー情報取得
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static getMeApiUsersMeGet(): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/me',
        });
    }
    /**
     * Get User
     * ユーザー詳細取得（本部管理者のみ）
     * @param userId
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static getUserApiUsersUserIdGet(
        userId: number,
    ): CancelablePromise<UserResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/{user_id}',
            path: {
                'user_id': userId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Department Users
     * 部門メンバー一覧取得
     * @param departmentId
     * @returns UserResponse Successful Response
     * @throws ApiError
     */
    public static getDepartmentUsersApiUsersDepartmentDepartmentIdGet(
        departmentId: number,
    ): CancelablePromise<Array<UserResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/users/department/{department_id}',
            path: {
                'department_id': departmentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Project
     * 案件申請（申請者のみ）
     * @param requestBody
     * @returns ProjectResponse Successful Response
     * @throws ApiError
     */
    public static createProjectApiProjectsPost(
        requestBody: ProjectCreate,
    ): CancelablePromise<ProjectResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Projects
     * 案件一覧取得（ロール別）
     * @param page
     * @param limit
     * @param status
     * @param keyword
     * @param departmentId
     * @param budgetMin
     * @param budgetMax
     * @param sortBy
     * @param sortOrder
     * @param alertLevel
     * @returns ProjectListResponse Successful Response
     * @throws ApiError
     */
    public static getProjectsApiProjectsGet(
        page: number = 1,
        limit: number = 10,
        status?: (Array<string> | null),
        keyword?: (string | null),
        departmentId?: (number | null),
        budgetMin?: (number | null),
        budgetMax?: (number | null),
        sortBy?: (string | null),
        sortOrder: string = 'desc',
        alertLevel?: (string | null),
    ): CancelablePromise<ProjectListResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects',
            query: {
                'page': page,
                'limit': limit,
                'status': status,
                'keyword': keyword,
                'department_id': departmentId,
                'budget_min': budgetMin,
                'budget_max': budgetMax,
                'sort_by': sortBy,
                'sort_order': sortOrder,
                'alert_level': alertLevel,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Budget Summary
     * 予算サマリー取得（部門管理者・本部管理者のみ）
     * @param status
     * @param keyword
     * @param departmentId
     * @param budgetMin
     * @param budgetMax
     * @returns BudgetSummaryResponse Successful Response
     * @throws ApiError
     */
    public static getBudgetSummaryApiProjectsBudgetSummaryGet(
        status?: (Array<string> | null),
        keyword?: (string | null),
        departmentId?: (number | null),
        budgetMin?: (number | null),
        budgetMax?: (number | null),
    ): CancelablePromise<BudgetSummaryResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/budget-summary',
            query: {
                'status': status,
                'keyword': keyword,
                'department_id': departmentId,
                'budget_min': budgetMin,
                'budget_max': budgetMax,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Project
     * 案件詳細取得
     * @param projectId
     * @returns ProjectResponse Successful Response
     * @throws ApiError
     */
    public static getProjectApiProjectsProjectIdGet(
        projectId: number,
    ): CancelablePromise<ProjectResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{project_id}',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Project
     * 案件更新（申請者のみ・承認待ち状態のみ）
     * @param projectId
     * @param requestBody
     * @returns ProjectResponse Successful Response
     * @throws ApiError
     */
    public static updateProjectApiProjectsProjectIdPut(
        projectId: number,
        requestBody: ProjectUpdate,
    ): CancelablePromise<ProjectResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/projects/{project_id}',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Approve Project
     * 案件承認・却下（部門管理者・本部管理者のみ）
     * @param projectId
     * @param requestBody
     * @returns ProjectResponse Successful Response
     * @throws ApiError
     */
    public static approveProjectApiProjectsProjectIdApprovePost(
        projectId: number,
        requestBody: ApprovalRequest,
    ): CancelablePromise<ProjectResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{project_id}/approve',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Start Project
     * 案件着手
     * @param projectId
     * @returns ProjectResponse Successful Response
     * @throws ApiError
     */
    public static startProjectApiProjectsProjectIdStartPatch(
        projectId: number,
    ): CancelablePromise<ProjectResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/projects/{project_id}/start',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Complete Project
     * 案件完了
     * @param projectId
     * @returns ProjectResponse Successful Response
     * @throws ApiError
     */
    public static completeProjectApiProjectsProjectIdCompletePatch(
        projectId: number,
    ): CancelablePromise<ProjectResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/projects/{project_id}/complete',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Task
     * タスク作成
     * @param projectId
     * @param requestBody
     * @returns TaskResponse Successful Response
     * @throws ApiError
     */
    public static createTask(
        projectId: number,
        requestBody: TaskCreate,
    ): CancelablePromise<TaskResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{project_id}/tasks',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Tasks
     * タスク一覧取得
     * @param projectId
     * @returns TaskResponse Successful Response
     * @throws ApiError
     */
    public static listTasks(
        projectId: number,
    ): CancelablePromise<Array<TaskResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{project_id}/tasks',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Task
     * タスク更新
     * @param projectId
     * @param taskId
     * @param requestBody
     * @returns TaskResponse Successful Response
     * @throws ApiError
     */
    public static updateTask(
        projectId: number,
        taskId: number,
        requestBody: TaskUpdate,
    ): CancelablePromise<TaskResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/projects/{project_id}/tasks/{task_id}',
            path: {
                'project_id': projectId,
                'task_id': taskId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Task
     * タスク削除
     * @param projectId
     * @param taskId
     * @returns void
     * @throws ApiError
     */
    public static deleteTask(
        projectId: number,
        taskId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/projects/{project_id}/tasks/{task_id}',
            path: {
                'project_id': projectId,
                'task_id': taskId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get All Tasks
     * 本部管理者用 全案件タスク取得
     * @returns TaskResponse Successful Response
     * @throws ApiError
     */
    public static getAllTasks(): CancelablePromise<Array<TaskResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/tasks/all',
        });
    }
    /**
     * Get Alerts
     * ダッシュボードアラート取得（本部・部門管理者用）
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getAlertsApiDashboardAlertsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/dashboard/alerts',
        });
    }
    /**
     * Dashboard
     * @returns any Successful Response
     * @throws ApiError
     */
    public static dashboardApiDashboardGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/dashboard',
        });
    }
    /**
     * Create Budget
     * 予算登録
     * @param projectId
     * @param requestBody
     * @returns ProjectBudgetResponse Successful Response
     * @throws ApiError
     */
    public static createBudget(
        projectId: number,
        requestBody: ProjectBudgetCreate,
    ): CancelablePromise<ProjectBudgetResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{project_id}/budget',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Budget
     * 予算取得
     * @param projectId
     * @returns ProjectBudgetResponse Successful Response
     * @throws ApiError
     */
    public static getBudget(
        projectId: number,
    ): CancelablePromise<ProjectBudgetResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{project_id}/budget',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Budget
     * 予算更新
     * @param projectId
     * @param requestBody
     * @returns ProjectBudgetResponse Successful Response
     * @throws ApiError
     */
    public static updateBudget(
        projectId: number,
        requestBody: ProjectBudgetUpdate,
    ): CancelablePromise<ProjectBudgetResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/projects/{project_id}/budget',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Worklog
     * 工数実績登録
     * @param projectId
     * @param requestBody
     * @returns WorklogResponse Successful Response
     * @throws ApiError
     */
    public static createWorklog(
        projectId: number,
        requestBody: WorklogCreate,
    ): CancelablePromise<WorklogResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{project_id}/worklogs',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Worklogs
     * 工数実績一覧取得
     * @param projectId
     * @returns WorklogResponse Successful Response
     * @throws ApiError
     */
    public static getWorklogs(
        projectId: number,
    ): CancelablePromise<Array<WorklogResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{project_id}/worklogs',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Worklog
     * 工数実績更新
     * @param projectId
     * @param worklogId
     * @param requestBody
     * @returns WorklogResponse Successful Response
     * @throws ApiError
     */
    public static updateWorklog(
        projectId: number,
        worklogId: number,
        requestBody: WorklogUpdate,
    ): CancelablePromise<WorklogResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/projects/{project_id}/worklogs/{worklog_id}',
            path: {
                'project_id': projectId,
                'worklog_id': worklogId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Worklog
     * 工数実績削除
     * @param projectId
     * @param worklogId
     * @returns void
     * @throws ApiError
     */
    public static deleteWorklog(
        projectId: number,
        worklogId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/projects/{project_id}/worklogs/{worklog_id}',
            path: {
                'project_id': projectId,
                'worklog_id': worklogId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Expense
     * 直接経費登録
     * @param projectId
     * @param requestBody
     * @returns ExpenseResponse Successful Response
     * @throws ApiError
     */
    public static createExpense(
        projectId: number,
        requestBody: ExpenseCreate,
    ): CancelablePromise<ExpenseResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/projects/{project_id}/expenses',
            path: {
                'project_id': projectId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Expenses
     * 直接経費一覧取得
     * @param projectId
     * @returns ExpenseResponse Successful Response
     * @throws ApiError
     */
    public static getExpenses(
        projectId: number,
    ): CancelablePromise<Array<ExpenseResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/projects/{project_id}/expenses',
            path: {
                'project_id': projectId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Expense
     * 直接経費更新
     * @param projectId
     * @param expenseId
     * @param requestBody
     * @returns ExpenseResponse Successful Response
     * @throws ApiError
     */
    public static updateExpense(
        projectId: number,
        expenseId: number,
        requestBody: ExpenseUpdate,
    ): CancelablePromise<ExpenseResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/projects/{project_id}/expenses/{expense_id}',
            path: {
                'project_id': projectId,
                'expense_id': expenseId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Expense
     * 直接経費削除
     * @param projectId
     * @param expenseId
     * @returns void
     * @throws ApiError
     */
    public static deleteExpense(
        projectId: number,
        expenseId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/projects/{project_id}/expenses/{expense_id}',
            path: {
                'project_id': projectId,
                'expense_id': expenseId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Notifications
     * 通知一覧取得
     * @param page
     * @param limit
     * @returns NotificationListResponse Successful Response
     * @throws ApiError
     */
    public static getNotificationsApiNotificationsGet(
        page: number = 1,
        limit: number = 10,
    ): CancelablePromise<NotificationListResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/notifications',
            query: {
                'page': page,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Mark As Read
     * 通知を既読にする
     * @param notificationId
     * @returns NotificationResponse Successful Response
     * @throws ApiError
     */
    public static markAsReadApiNotificationsNotificationIdReadPut(
        notificationId: number,
    ): CancelablePromise<NotificationResponse> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/notifications/{notification_id}/read',
            path: {
                'notification_id': notificationId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Mark All As Read
     * 全通知を既読にする
     * @returns void
     * @throws ApiError
     */
    public static markAllAsReadApiNotificationsReadAllPut(): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/notifications/read-all',
        });
    }
    /**
     * Get Departments
     * 部門一覧取得（全ロール対応）
     * @returns DepartmentResponse Successful Response
     * @throws ApiError
     */
    public static getDepartmentsApiDepartmentsGet(): CancelablePromise<Array<DepartmentResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/departments',
        });
    }
    /**
     * Get Department Tasks
     * 部門内の全タスク一覧取得
     * @param departmentId
     * @returns TaskResponse Successful Response
     * @throws ApiError
     */
    public static getDepartmentTasks(
        departmentId: number,
    ): CancelablePromise<Array<TaskResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/departments/{department_id}/tasks',
            path: {
                'department_id': departmentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
