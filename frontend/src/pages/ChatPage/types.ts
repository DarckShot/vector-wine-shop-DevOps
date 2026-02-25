import type { Wine } from "../../api/api.types";

export type ChatMessage = {
  id: string;
  role: "user" | "bot";
  text: string;
  wines?: Wine[];
};

export type FieldKeys = "value" | "minPrice" | "maxPrice";

export type FieldState = Record<FieldKeys, boolean>;
