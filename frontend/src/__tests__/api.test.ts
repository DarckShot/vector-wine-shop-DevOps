import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

describe("api helpers", () => {
  let post: ReturnType<typeof vi.fn>;
  let get: ReturnType<typeof vi.fn>;
  let put: ReturnType<typeof vi.fn>;
  let del: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    post = vi.fn();
    get = vi.fn();
    put = vi.fn();
    del = vi.fn();

    // doMock is not hoisted, safe to call here
    vi.doMock("axios", () => ({
      default: {
        create: () => ({ post, get, put, delete: del }),
      },
    }));
  });

  afterEach(() => {
    vi.resetModules();
  });

  it("searchWines posts and returns data", async () => {
    const api = await import("../api/api");
    const sample = { results: [] };
    post.mockResolvedValueOnce({ data: sample });

    const res = await api.searchWines({ q: "a" } as any);
    expect(post).toHaveBeenCalled();
    expect(res).toBe(sample);
  });

  it("addWineToCart calls post and returns void", async () => {
    const api = await import("../api/api");
    post.mockResolvedValueOnce({});
    await expect(api.addWineToCart("id-1" as any)).resolves.toBeUndefined();
    expect(post).toHaveBeenCalled();
  });

  it("getCartWines calls get and returns data", async () => {
    const api = await import("../api/api");
    const sample = { items: [] };
    get.mockResolvedValueOnce({ data: sample });
    const res = await api.getCartWines();
    expect(get).toHaveBeenCalled();
    expect(res).toBe(sample);
  });

  it("updateCartWineCount calls put and returns data", async () => {
    const api = await import("../api/api");
    const sample = { ok: true };
    put.mockResolvedValueOnce({ data: sample });
    const res = await api.updateCartWineCount("id", { count: 2 } as any);
    expect(put).toHaveBeenCalled();
    expect(res).toBe(sample);
  });

  it("deleteWineFromCart calls delete and returns void", async () => {
    const api = await import("../api/api");
    del.mockResolvedValueOnce({});
    await expect(api.deleteWineFromCart("id")).resolves.toBeUndefined();
    expect(del).toHaveBeenCalled();
  });
});
