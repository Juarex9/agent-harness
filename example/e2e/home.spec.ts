import { expect, test } from "@playwright/test";

test("la home muestra el título y el precio de ejemplo", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "Plantilla Harness" }),
  ).toBeVisible();
  await expect(page.getByTestId("precio-ejemplo")).toContainText("$");
});
