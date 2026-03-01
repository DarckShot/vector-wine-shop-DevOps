import { describe, it, expect } from "vitest";
import { formatPrice } from "../pages/ChatPage/utils/formatPrice";

describe("formatPrice", () => {
  it("formats finite numbers with ₽ and thousands separator", () => {
    expect(formatPrice(12345)).toContain("₽");
    expect(formatPrice(12345)).toMatch(/12.?345/); // locale may add NBSP
  });

  it("returns placeholder for NaN or Infinity", () => {
    expect(formatPrice(Number.NaN)).toBe("— ₽");
    expect(formatPrice(Number.POSITIVE_INFINITY)).toBe("— ₽");
  });
});
