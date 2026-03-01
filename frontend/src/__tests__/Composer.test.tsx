import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Composer from "../pages/ChatPage/components/Composer";

describe("Composer component", () => {
  it("renders inputs and calls onSend when valid", () => {
    const setValue = vi.fn();
    const setMin = vi.fn();
    const setMax = vi.fn();
    const onSend = vi.fn();

    render(
      <Composer
        value={"hello"}
        setValue={setValue}
        minPrice={"0"}
        setMinPrice={setMin}
        maxPrice={"10"}
        setMaxPrice={setMax}
        loading={false}
        onSend={onSend}
        onKeyDown={() => {}}
      />,
    );

    expect(screen.getByLabelText("Сообщение")).toBeInTheDocument();
    expect(screen.getByLabelText("Минимальная цена")).toBeInTheDocument();
    expect(screen.getByLabelText("Максимальная цена")).toBeInTheDocument();

    const btn = screen.getByLabelText("Отправить сообщение");
    fireEvent.click(btn);

    // onSend should be called via the hook when fields are valid
    expect(onSend).toHaveBeenCalled();
  });

  it("disables send button when loading", () => {
    const setValue = vi.fn();
    const setMin = vi.fn();
    const setMax = vi.fn();
    const onSend = vi.fn();

    render(
      <Composer
        value={""}
        setValue={setValue}
        minPrice={""}
        setMinPrice={setMin}
        maxPrice={""}
        setMaxPrice={setMax}
        loading={true}
        onSend={onSend}
        onKeyDown={() => {}}
      />,
    );

    const btns = screen.getAllByLabelText(
      "Отправить сообщение",
    ) as HTMLButtonElement[];
    const disabled = btns.find((b) => b.disabled);
    expect(disabled).toBeDefined();
  });
});
