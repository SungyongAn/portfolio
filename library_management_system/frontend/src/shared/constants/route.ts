import type { Role } from "@/domains/user/types";

export const ROLE_DEFAULT_ROUTE: Record<Role, string> = {
  student: "/dashboard",
  librarian: "/librarian/dashboard",
  admin: "/admin/dashboard",
};

export const LOGIN_ROUTE = "/login";
