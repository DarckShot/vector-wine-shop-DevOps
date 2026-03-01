import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import GlobalPageWrapper from "../components/GlobalPageWrapper/GlobalPageWrapper";

describe("GlobalPageWrapper", () => {
  it("renders children inside container", () => {
    render(
      <GlobalPageWrapper>
        <div>Inner</div>
      </GlobalPageWrapper>,
    );

    expect(screen.getByText("Inner")).toBeInTheDocument();
  });
});
