import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import App from "../App";

describe("App", () => {
  it("renders Chat page by default", () => {
    // polyfill scrollTo used by ChatPage
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (global as any).HTMLElement.prototype.scrollTo = () => {};

    render(<App />);
    // Header title 'Чат' should be present from ChatPage
    expect(screen.getByText("Чат")).toBeInTheDocument();
  });
});
