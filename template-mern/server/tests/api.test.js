import { describe, expect, it } from "vitest";
import request from "supertest";
import { app } from "../server.js";

describe("API", () => {
  it("GET /api/health responde ok", async () => {
    const res = await request(app).get("/api/health");
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: "ok" });
  });

  it("GET /api/saludo sin name saluda mundo", async () => {
    const res = await request(app).get("/api/saludo");
    expect(res.body).toEqual({ saludo: "Hola, mundo" });
  });

  it("GET /api/saludo?name=Ana saluda Ana", async () => {
    const res = await request(app).get("/api/saludo?name=Ana");
    expect(res.body).toEqual({ saludo: "Hola, Ana" });
  });

  it("el nombre con HTML viaja literal en el JSON", async () => {
    const res = await request(app).get("/api/saludo?name=%3Cb%3EAna%3C%2Fb%3E");
    expect(res.body).toEqual({ saludo: "Hola, <b>Ana</b>" });
  });
});
