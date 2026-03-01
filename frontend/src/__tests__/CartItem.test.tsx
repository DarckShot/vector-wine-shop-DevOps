import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import CartItem from "../pages/CartPage/components/CartItem";

const sampleWine = {
  id: "w1",
  name: "Test Wine",
  country: "RU",
  color: "red",
  acidity: "medium",
  price: 1000,
  count: 2,
  description: "desc",
};

describe("CartItem", () => {
  it("renders wine info and responds to buttons", () => {
    const onInc = vi.fn();
    const onDec = vi.fn();
    const onRemove = vi.fn();

    render(
      <CartItem
        wine={sampleWine as any}
        onIncrease={onInc}
        onDecrease={onDec}
        onRemove={onRemove}
      />,
    );

    expect(screen.getByText("Test Wine")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();

    const plus = screen.getByLabelText(/Увеличить Test Wine/);
    const minus = screen.getByLabelText(/Уменьшить Test Wine/);
    const remove = screen.getByLabelText(/Удалить Test Wine/);

    fireEvent.click(plus);
    expect(onInc).toHaveBeenCalledWith("w1");

    fireEvent.click(minus);
    expect(onDec).toHaveBeenCalledWith("w1");

    fireEvent.click(remove);
    expect(onRemove).toHaveBeenCalledWith("w1");
  });
});
