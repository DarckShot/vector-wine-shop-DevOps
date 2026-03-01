import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import MessageBubble from "../pages/ChatPage/components/MessageBubble";

const msgWithWine = {
  role: "bot",
  text: "Here is a wine",
  wines: [
    {
      id: "w1",
      name: "Wine 1",
      country: "RU",
      color: "white",
      acidity: "low",
      price: 500,
      description: "tasty",
    },
  ],
};

describe("MessageBubble", () => {
  it("renders message text and wine cards with add handler", () => {
    const onAdd = vi.fn();
    render(<MessageBubble msg={msgWithWine as any} onAdd={onAdd} />);

    expect(screen.getByText("Here is a wine")).toBeInTheDocument();
    expect(screen.getByText("Wine 1")).toBeInTheDocument();

    const addBtn = screen.getByLabelText(/Добавить Wine 1/);
    fireEvent.click(addBtn);
    expect(onAdd).toHaveBeenCalledWith("w1");
  });
});
