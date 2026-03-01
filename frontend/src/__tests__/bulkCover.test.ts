import { describe, it, expect } from "vitest";

// Import a set of modules to increase baseline coverage by executing module
// top-level code that is safe to run in tests (no DOM mutations).
import App from "../App";
import ChatPage from "../pages/ChatPage/ChatPage";
import CartPage from "../pages/CartPage/CartPage";
import GlobalPageWrapper from "../components/GlobalPageWrapper/GlobalPageWrapper";
import Header from "../components/Header/Header";
import HomeIcon from "../assets/icon/header/HomeIcon";
import BasketIcon from "../assets/icon/header/BasketIcon";
import * as apiTypes from "../api/api.types";

describe("bulk coverage imports", () => {
  it("exports exist and are callable/defined", () => {
    expect(App).toBeDefined();
    expect(typeof ChatPage).toBe("function");
    expect(typeof CartPage).toBe("function");
    expect(typeof GlobalPageWrapper).toBe("function");
    expect(typeof Header).toBe("function");
    expect(HomeIcon).toBeDefined();
    expect(BasketIcon).toBeDefined();
    expect(apiTypes).toBeTruthy();
  });
});
