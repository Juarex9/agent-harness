import { describe, expect, it } from "vitest";
import { saludoUrl } from "./api.js";

describe("saludoUrl", () => {
  it("sin nombre apunta al endpoint base", () => {
    expect(saludoUrl(undefined)).toBe("/api/saludo");
    expect(saludoUrl("   ")).toBe("/api/saludo");
  });

  it("agrega el nombre como query param", () => {
    expect(saludoUrl("Ana")).toBe("/api/saludo?name=Ana");
  });

  it("recorta espacios y codifica HTML", () => {
    expect(saludoUrl("  Ana  ")).toBe("/api/saludo?name=Ana");
    expect(saludoUrl("<b>Ana</b>")).toBe("/api/saludo?name=%3Cb%3EAna%3C%2Fb%3E");
  });
});
