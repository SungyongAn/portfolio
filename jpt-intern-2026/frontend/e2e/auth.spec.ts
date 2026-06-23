import { test, expect } from "@playwright/test";
import { login, TEST_ACCOUNTS } from "./helpers/auth";

test.describe("ログイン", () => {
  test("APPLICANTでログインできる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.applicant;
    await login(page, email, password);
    await expect(page).toHaveURL("/");
    await expect(
      page.getByRole("heading", { name: "開発案件状況ダッシュボード" }),
    ).toBeVisible();
  });

  test("誤ったパスワードではログインできない", async ({ page }) => {
    await page.goto("/login");
    await page
      .getByPlaceholder("メールアドレス")
      .fill(TEST_ACCOUNTS.applicant.email);
    await page.getByPlaceholder("パスワード").fill("wrongpassword");
    await page.getByRole("button", { name: "ログイン" }).click();
    await expect(page.getByRole("alert")).toBeVisible();
  });

  test("未ログイン状態でダッシュボードへアクセスするとログイン画面へリダイレクト", async ({
    page,
  }) => {
    await page.goto("/");
    await expect(page).toHaveURL("/login");
  });
});
