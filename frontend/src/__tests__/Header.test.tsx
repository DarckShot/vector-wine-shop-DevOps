import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Header from "../components/Header/Header";

describe("Header", () => {
  it("renders title and link for basket variant", () => {
    render(
      <MemoryRouter>
        <Header title="My Title" variant="basket" />
      </MemoryRouter>,
    );

    expect(screen.getByText("My Title")).toBeInTheDocument();
    const link = screen.getByRole("link");
    expect(link).toBeInTheDocument();
  });

  it("renders link for chat variant", () => {
    render(
      <MemoryRouter>
        <Header title="Chat" variant="chat" />
      </MemoryRouter>,
    );

    expect(screen.getByText("Chat")).toBeInTheDocument();
    const links = screen.getAllByRole("link");
    // There may be multiple links in the page; ensure one points to /basket
    expect(
      links.some((l) =>
        (l as HTMLAnchorElement).getAttribute("href")?.includes("/basket"),
      ),
    ).toBe(true);
  });
});
