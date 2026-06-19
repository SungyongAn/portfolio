import { test, expect } from "@playwright/test";
import { login, TEST_ACCOUNTS } from "./helpers/auth";

test.describe("案件申請・承認フロー", () => {
  test("APPLICANTが案件を申請できる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.applicant;
    await login(page, email, password);

    // 案件申請画面へ遷移
    await page.goto("/projects/new");

    // フォーム入力
    await page.getByLabel("案件名").fill("E2Eテスト案件");
    await page.getByLabel("目的・概要").fill("E2Eテスト用の案件です");
    await page.getByLabel("概算予算").fill("1000000");
    await page.getByLabel("概算工数").fill("3");

    // 申請ボタンをクリック
    await page.getByRole("button", { name: "申請" }).click();

    // 申請成功の確認
    await expect(page.getByText("申請しました")).toBeVisible();
  });

  test("DEPT_MANAGERが一次承認できる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.deptManager;
    await login(page, email, password);

    // 承認待ち案件を開く
    await page.goto("/projects");
    await page.getByText("部門承認待ち").first().click();

    // 承認ボタンをクリック
    await page.getByRole("button", { name: "承認" }).click();
    await page.getByRole("button", { name: "確認" }).click();

    // 承認成功の確認
    await expect(page.getByText("承認しました")).toBeVisible();
  });

  test("HQ_MANAGERが最終承認できる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.hqManager;
    await login(page, email, password);

    // 承認待ち案件を開く
    await page.goto("/projects");
    await page.getByText("本部承認待ち").first().click();

    // 最終承認ボタンをクリック
    await page.getByRole("button", { name: "承認" }).click();
    await page.getByRole("button", { name: "確認" }).click();

    // 承認成功・ステータス変更の確認
    await expect(page.getByText("承認しました")).toBeVisible();
    await expect(page.getByText("承認済み")).toBeVisible();
  });
});
