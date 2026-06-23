import { Page } from "@playwright/test";

export const TEST_ACCOUNTS = {
  applicant: {
    email: "tanaka@nextflow.example.com",
    password: "password",
    role: "APPLICANT",
  },
  deptManager: {
    email: "yamada@nextflow.example.com",
    password: "password",
    role: "DEPT_MANAGER",
  },
  hqManager: {
    email: "takahashi@nextflow.example.com",
    password: "password",
    role: "HQ_MANAGER",
  },
  taskMember: {
    email: "kameda@nextflow.example.com",
    password: "password",
    role: "TASK_MEMBER",
  },
};

export const login = async (page: Page, email: string, password: string) => {
  await page.goto("/login");
  await page.getByLabel("メールアドレス").fill(email);
  await page.getByLabel("パスワード").fill(password);
  await page.getByRole("button", { name: "ログイン" }).click();
  await page.waitForURL("/");
};
