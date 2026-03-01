import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";

describe("useChat", () => {
  let searchWines: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    searchWines = vi.fn();
    vi.doMock("../api/api", () => ({ searchWines }));
  });

  afterEach(() => {
    vi.resetModules();
  });

  it("send adds user and bot messages on success", async () => {
    const api = await import("../api/api");
    searchWines.mockResolvedValueOnce({ summary: "ok", wines: [] });

    const { result } = await import("../pages/ChatPage/hooks/useChat").then(
      (m) => renderHook(() => m.useChat()),
    );

    // initial state
    expect(result.current.messages.length).toBe(0);

    // set value and wait for effect to update refs
    await act(async () => {
      result.current.setValue("hello");
      await Promise.resolve();
    });

    await act(async () => {
      await result.current.send();
    });

    expect(result.current.messages.length).toBeGreaterThanOrEqual(2);
    expect(searchWines).toHaveBeenCalled();
  });

  it("send handles errors and appends error bot message", async () => {
    searchWines.mockRejectedValueOnce(new Error("fail"));

    const { result } = await import("../pages/ChatPage/hooks/useChat").then(
      (m) => renderHook(() => m.useChat()),
    );

    await act(async () => {
      result.current.setValue("hello");
      await Promise.resolve();
    });

    await act(async () => {
      await result.current.send();
    });

    const last = result.current.messages[result.current.messages.length - 1];
    expect(last).toBeDefined();
    expect(last?.text).toContain("Ошибка");
  });
});
