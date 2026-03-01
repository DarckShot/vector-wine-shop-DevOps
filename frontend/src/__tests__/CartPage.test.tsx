import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";

describe("CartPage", () => {
  it("shows loading state when useCart reports loading", async () => {
    vi.resetModules();
    vi.doMock("../pages/CartPage/hooks/useCart", () => ({
      useCart: () => ({
        wines: [],
        loading: true,
        increase: () => {},
        decrease: () => {},
        remove: () => {},
      }),
    }));

    const { default: CartPage } = await import("../pages/CartPage/CartPage");
    const { MemoryRouter } = await import("react-router-dom");
    render(
      <MemoryRouter>
        <CartPage />
      </MemoryRouter>,
    );

    expect(screen.getByText("Загрузка...")).toBeInTheDocument();
  });

  it("shows empty message when no wines", async () => {
    vi.resetModules();
    vi.doMock("../pages/CartPage/hooks/useCart", () => ({
      useCart: () => ({
        wines: [],
        loading: false,
        increase: () => {},
        decrease: () => {},
        remove: () => {},
      }),
    }));

    const { default: CartPage } = await import("../pages/CartPage/CartPage");
    const { MemoryRouter } = await import("react-router-dom");
    render(
      <MemoryRouter>
        <CartPage />
      </MemoryRouter>,
    );

    expect(screen.getByText("Корзина пуста")).toBeInTheDocument();
  });

  it("renders a cart item when wines present", async () => {
    vi.resetModules();
    const wine = {
      id: "w1",
      name: "Test Wine",
      country: "X",
      color: "red",
      acidity: "medium",
      price: "100",
      count: 2,
    };
    vi.doMock("../pages/CartPage/hooks/useCart", () => ({
      useCart: () => ({
        wines: [wine],
        loading: false,
        increase: () => {},
        decrease: () => {},
        remove: () => {},
      }),
    }));

    const { default: CartPage } = await import("../pages/CartPage/CartPage");
    const { MemoryRouter } = await import("react-router-dom");
    render(
      <MemoryRouter>
        <CartPage />
      </MemoryRouter>,
    );

    expect(screen.getByText("Test Wine")).toBeInTheDocument();
  });
});
