import { test, expect } from "@playwright/test";
import { login, TEST_ACCOUNTS } from "./helpers/auth";

test.describe("予算・工数入力", () => {
  test("APPLICANTが工数実績を入力できる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.applicant;
    await login(page, email, password);

    // 承認済み案件の予算管理画面へ遷移
    await page.goto("/projects");
    await page.getByText("進行中").first().click();
    await page.getByRole("button", { name: "予算管理" }).click();

    // 工数実績入力
    await page.getByRole("button", { name: "工数実績入力" }).click();
    await page.getByLabel("対象月").fill("2026-06");
    await page.getByLabel("実績工数").fill("1.5");
    await page.getByRole("button", { name: "登録" }).click();

    // 登録成功の確認
    await expect(page.getByText("登録しました")).toBeVisible();
  });
});
