import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useComposer } from "../pages/ChatPage/hooks/useComposer";

describe("useComposer", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });
  afterEach(() => {
    vi.useRealTimers();
  });

  it("validates missing fields and triggers shakes", () => {
    const setValue = vi.fn();
    const setMin = vi.fn();
    const setMax = vi.fn();
    const onSend = vi.fn();

    const { result } = renderHook(() =>
      useComposer({
        value: "",
        setValue,
        minPrice: "",
        setMinPrice: setMin,
        maxPrice: "",
        setMaxPrice: setMax,
        onSend,
      }),
    );

    act(() => {
      result.current.handleSend();
    });

    expect(result.current.submittedOnce).toBe(true);
    expect(result.current.errors.value).toBe(true);
    expect(result.current.errors.minPrice).toBe(true);
    expect(result.current.errors.maxPrice).toBe(true);

    // advance timers to clear shakes
    act(() => {
      vi.runAllTimers();
    });

    expect(result.current.shakes.value).toBe(false);
  });

  it("onValueChange clears value error and calls setValue", () => {
    const setValue = vi.fn();
    const setMin = vi.fn();
    const setMax = vi.fn();
    const onSend = vi.fn();

    const { result } = renderHook(() =>
      useComposer({
        value: "a",
        setValue,
        minPrice: "0",
        setMinPrice: setMin,
        maxPrice: "10",
        setMaxPrice: setMax,
        onSend,
      }),
    );

    act(() => {
      result.current.setErrors({
        value: true,
        minPrice: false,
        maxPrice: false,
      });
    });

    act(() => {
      result.current.onValueChange({ target: { value: "b" } } as any);
    });

    expect(setValue).toHaveBeenCalledWith("b");
    expect(result.current.errors.value).toBe(false);
  });
});
