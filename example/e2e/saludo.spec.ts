import { expect, test } from "@playwright/test";

test("saludo sin name muestra Hola, mundo", async ({ page }) => {
  await page.goto("/saludo");

  await expect(page.getByRole("heading", { name: "Hola, mundo" })).toBeVisible();
});

test("saludo con name=Ana muestra Hola, Ana", async ({ page }) => {
  await page.goto("/saludo?name=Ana");

  await expect(page.getByRole("heading", { name: "Hola, Ana" })).toBeVisible();
});

test("el nombre con HTML se muestra como texto exacto, sin inyectar", async ({
  page,
}) => {
  await page.goto("/saludo?name=%3Cb%3EAna%3C%2Fb%3E");

  await expect(
    page.getByRole("heading", { name: "Hola, <b>Ana</b>", exact: true }),
  ).toBeVisible();
  await expect(page.locator("h1 b")).toHaveCount(0);
});
