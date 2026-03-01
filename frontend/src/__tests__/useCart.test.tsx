import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import React from "react";

describe("useCart", () => {
  let getCartWines: ReturnType<typeof vi.fn>;
  let updateCartWineCount: ReturnType<typeof vi.fn>;
  let deleteWineFromCart: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    getCartWines = vi.fn();
    updateCartWineCount = vi.fn();
    deleteWineFromCart = vi.fn();

    vi.doMock("../api/api", () => ({
      getCartWines,
      updateCartWineCount,
      deleteWineFromCart,
    }));
  });

  afterEach(() => {
    vi.resetModules();
  });

  it("loads wines and responds to increase/decrease/remove", async () => {
    const sample = {
      wines: [
        {
          id: "a",
          name: "A",
          price: 10,
          count: 1,
          country: "RU",
          color: "red",
          acidity: "med",
        },
      ],
    };
    getCartWines.mockResolvedValueOnce(sample);
    updateCartWineCount.mockResolvedValue({ updatedCount: 2 });
    deleteWineFromCart.mockResolvedValue({});

    const { default: ReactModule } = await import("react");
    const { useCart } = await import("../pages/CartPage/hooks/useCart");

    function TestComponent() {
      const { wines, loading, increase, decrease, remove } = useCart();
      return (
        <div>
          <div>{loading ? "LOADING" : "READY"}</div>
          {wines.map((w) => (
            <div key={w.id} data-testid={`wine-${w.id}`}>
              <span>{w.name}</span>
              <button onClick={() => increase(w.id)}>inc</button>
              <button onClick={() => decrease(w.id)}>dec</button>
              <button onClick={() => remove(w.id)}>rm</button>
            </div>
          ))}
        </div>
      );
    }

    const { rerender } = render(<TestComponent />);

    await waitFor(() => expect(getCartWines).toHaveBeenCalled());
    expect(screen.getByText("A")).toBeInTheDocument();

    fireEvent.click(screen.getByText("inc"));
    await waitFor(() => expect(updateCartWineCount).toHaveBeenCalled());

    fireEvent.click(screen.getByText("dec"));
    await waitFor(() => expect(updateCartWineCount).toHaveBeenCalled());

    fireEvent.click(screen.getByText("rm"));
    await waitFor(() => expect(deleteWineFromCart).toHaveBeenCalled());
  });
});
