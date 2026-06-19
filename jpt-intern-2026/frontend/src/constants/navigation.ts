import type { Component } from "vue";
import {
  House,
  List,
  Document,
  Money,
  Loading,
  User,
} from "@element-plus/icons-vue";

export type MenuItem = {
  label: string;
  to: string;
  icon: Component;
};

export const menuMap: Record<string, MenuItem[]> = {
  TASK_MEMBER: [
    { label: "ダッシュボード", to: "/", icon: House },
    {
      label: "案件一覧",
      to: "/?view=projects",
      icon: Loading,
    },
  ],

  APPLICANT: [
    { label: "ダッシュボード", to: "/", icon: House },

    {
      label: "案件一覧",
      to: "/?view=projects",
      icon: Loading,
    },

    {
      label: "案件申請",
      to: "/?action=create-project",
      icon: Document,
    },
  ],

  DEPT_MANAGER: [
    { label: "ダッシュボード", to: "/", icon: House },
    { label: "案件一覧", to: "/projects", icon: List },
    { label: "予算管理", to: "/budget", icon: Money },
    { label: "メンバー状況", to: "/members/tasks", icon: User },
  ],

  HQ_MANAGER: [
    { label: "ダッシュボード", to: "/", icon: House },
    { label: "案件一覧", to: "/projects", icon: List },
    { label: "予算管理", to: "/budget", icon: Money },
  ],
};
