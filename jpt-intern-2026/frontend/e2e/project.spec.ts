import { test, expect } from "@playwright/test";
import { login, TEST_ACCOUNTS } from "./helpers/auth";

test.describe("案件申請・承認フロー", () => {
  test("APPLICANTが案件を申請できる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.applicant;
    await login(page, email, password);

    await page.goto("/projects/new");

    await page.getByLabel("案件名").fill("E2Eテスト案件");
    await page.getByLabel("目的・概要").fill("E2Eテスト用の案件です");
    await page.getByLabel("概算予算（円）").clear();
    await page.getByLabel("概算予算（円）").type("1000000");
    await page.getByLabel("概算工数（人月）").clear();
    await page.getByLabel("概算工数（人月）").type("3");

    await page.getByRole("button", { name: "申請する" }).click();

    await expect(page.getByText("案件を申請しました")).toBeVisible();
  });

  test("DEPT_MANAGERが一次承認できる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.deptManager;
    await login(page, email, password);

    await page.goto("/projects");
    await page.getByText("部門承認待ち").first().locator("..").click();

    await page.getByRole("button", { name: "承認" }).click();
    await page.getByRole("button", { name: "確認" }).click();

    await expect(page.getByText("承認しました")).toBeVisible();
  });

  test("HQ_MANAGERが最終承認できる", async ({ page }) => {
    const { email, password } = TEST_ACCOUNTS.hqManager;
    await login(page, email, password);

    await page.goto("/projects");
    await page.getByText("本部承認待ち").first().locator("..").click();

    await page.getByRole("button", { name: "承認" }).click();
    await page.getByRole("button", { name: "確認" }).click();

    await expect(page.getByText("承認しました")).toBeVisible();
    await expect(page.getByText("承認済み")).toBeVisible();
  });
});
