import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";

describe("ChatPage", () => {
  it("renders loading indicator when loading", async () => {
    vi.resetModules();
    vi.doMock("../pages/ChatPage/hooks/useChat", () => ({
      useChat: () => ({
        messages: [],
        value: "",
        setValue: () => {},
        minPrice: "",
        setMinPrice: () => {},
        maxPrice: "",
        setMaxPrice: () => {},
        loading: true,
        send: async () => {},
      }),
    }));

    const { default: ChatPage } = await import("../pages/ChatPage/ChatPage");
    const { MemoryRouter } = await import("react-router-dom");
    // polyfill scrollTo used in ChatPage
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (global as any).HTMLElement.prototype.scrollTo = () => {};
    render(
      <MemoryRouter>
        <ChatPage />
      </MemoryRouter>,
    );

    expect(screen.getByText("Отправка...")).toBeInTheDocument();
  });

  it("renders messages when provided by useChat", async () => {
    vi.resetModules();
    const msg = { id: "1", role: "user", text: "hi" };
    vi.doMock("../pages/ChatPage/hooks/useChat", () => ({
      useChat: () => ({
        messages: [msg],
        value: "",
        setValue: () => {},
        minPrice: "",
        setMinPrice: () => {},
        maxPrice: "",
        setMaxPrice: () => {},
        loading: false,
        send: async () => {},
      }),
    }));

    const { default: ChatPage } = await import("../pages/ChatPage/ChatPage");
    const { MemoryRouter } = await import("react-router-dom");
    // polyfill scrollTo used in ChatPage
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (global as any).HTMLElement.prototype.scrollTo = () => {};
    render(
      <MemoryRouter>
        <ChatPage />
      </MemoryRouter>,
    );

    expect(screen.getByText("hi")).toBeInTheDocument();
  });

  it("calls send on Enter key and addWineToCart when clicking add", async () => {
    vi.resetModules();
    const send = vi.fn();
    const addWineToCart = vi.fn();

    const wine = {
      id: "wine-1",
      name: "SomeWine",
      country: "C",
      color: "white",
      acidity: "low",
      price: "200",
    };
    const msg = { id: "1", role: "bot", text: "result", wines: [wine] };

    vi.doMock("../pages/ChatPage/hooks/useChat", () => ({
      useChat: () => ({
        messages: [msg],
        value: "",
        setValue: () => {},
        minPrice: "",
        setMinPrice: () => {},
        maxPrice: "",
        setMaxPrice: () => {},
        loading: false,
        send,
      }),
    }));

    vi.doMock("../api/api", () => ({ addWineToCart }));

    const { default: ChatPage } = await import("../pages/ChatPage/ChatPage");
    const { MemoryRouter } = await import("react-router-dom");
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (global as any).HTMLElement.prototype.scrollTo = () => {};

    render(
      <MemoryRouter>
        <ChatPage />
      </MemoryRouter>,
    );

    const textareas = screen.getAllByLabelText("Сообщение");
    const textarea = textareas[textareas.length - 1];
    fireEvent.keyDown(textarea, {
      key: "Enter",
      code: "Enter",
      charCode: 13,
      shiftKey: false,
    });
    expect(send).toHaveBeenCalled();

    // click the add button rendered by WineCard
    const addBtns = screen.getAllByLabelText("Добавить SomeWine");
    const addBtn = addBtns[addBtns.length - 1];
    fireEvent.click(addBtn);
    expect(addWineToCart).toHaveBeenCalledWith("wine-1");
  });
});
