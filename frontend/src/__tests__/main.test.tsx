import { describe, it, expect } from "vitest";

describe("main entry", () => {
  it("mounts App into #root without throwing", async () => {
    // create a root element similar to index.html
    document.body.innerHTML = '<div id="root"></div>';

    // polyfill scrollTo used by ChatPage
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (globalThis as any).HTMLElement.prototype.scrollTo = () => {};

    // import dynamically to execute top-level createRoot call
    await import("../main");

    const root = document.getElementById("root");
    expect(root).toBeTruthy();
  });
});
