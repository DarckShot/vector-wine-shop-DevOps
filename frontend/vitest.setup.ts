import * as matchers from "@testing-library/jest-dom/matchers";
import { expect } from "vitest";

if (matchers && typeof matchers === "object") {
  // Extend Vitest's expect with Testing Library matchers when available
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  expect.extend(matchers as any);
}
