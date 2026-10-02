import { describe, expect, it } from "vitest";
import { formatCurrency } from "@/lib/format";

describe("formatCurrency", () => {
  it("formatea un monto en pesos argentinos", () => {
    expect(formatCurrency(1999.5)).toBe("$ 1.999,50");
  });

  it("formatea el cero", () => {
    expect(formatCurrency(0)).toBe("$ 0,00");
  });

  it("rechaza valores no finitos", () => {
    expect(() => formatCurrency(NaN)).toThrow("número finito");
    expect(() => formatCurrency(Infinity)).toThrow("número finito");
  });
});
