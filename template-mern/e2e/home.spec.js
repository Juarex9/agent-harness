import { expect, test } from "@playwright/test";

test("la home muestra el título", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "Plantilla MERN" }),
  ).toBeVisible();
});
