import { describe, expect, it } from "vitest";
import { greet } from "@/lib/greet";

describe("greet", () => {
  it("saluda un nombre normal", () => {
    expect(greet("Ana")).toBe("Hola, Ana");
  });

  it("saluda mundo cuando el nombre es undefined", () => {
    expect(greet(undefined)).toBe("Hola, mundo");
  });

  it("saluda mundo cuando el nombre está vacío", () => {
    expect(greet("")).toBe("Hola, mundo");
  });

  it("saluda mundo cuando el nombre tiene solo espacios", () => {
    expect(greet("   ")).toBe("Hola, mundo");
  });

  it("recorta los espacios alrededor del nombre", () => {
    expect(greet("  Ana  ")).toBe("Hola, Ana");
  });
});
