import { describe, it, expect, vi } from "vitest";
import type { ChangeEvent } from "react";
import {
  isBlank,
  getFieldClass,
  makePriceChangeHandler,
} from "../pages/ChatPage/utils/composerUtils";

describe("composerUtils", () => {
  it("isBlank detects empty/whitespace", () => {
    expect(isBlank()).toBe(true);
    expect(isBlank(null)).toBe(true);
    expect(isBlank("   ")).toBe(true);
    expect(isBlank("ok")).toBe(false);
  });

  it("getFieldClass concatenates classes correctly", () => {
    const res = getFieldClass("base", true, false, "err", "shake");
    expect(res).toBe("base err");

    const res2 = getFieldClass("base", false, true, "err", "shake");
    expect(res2).toBe("base shake");
  });

  it("makePriceChangeHandler calls setPrice and clearError", () => {
    const setPrice = vi.fn();
    const clearError = vi.fn();
    const handler = makePriceChangeHandler(setPrice, clearError);

    handler({
      target: { value: "100" },
    } as unknown as ChangeEvent<HTMLInputElement>);

    expect(setPrice).toHaveBeenCalledWith("100");
    expect(clearError).toHaveBeenCalled();
  });
});
