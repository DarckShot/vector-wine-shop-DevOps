import type { ChangeEvent } from "react";

export const isBlank = (v?: string | null) =>
  v === undefined || v === null || String(v).trim() === "";

export function getFieldClass(
  baseClass: string,
  hasError: boolean,
  isShaking: boolean,
  inputErrorClass: string,
  shakeClass: string,
) {
  return (
    baseClass +
    (hasError ? ` ${inputErrorClass}` : "") +
    (isShaking ? ` ${shakeClass}` : "")
  );
}

export function makePriceChangeHandler(
  setPrice: (v: string) => void,
  clearError?: () => void,
) {
  return (e: ChangeEvent<HTMLInputElement>) => {
    setPrice(e.target.value);
    if (clearError) clearError();
  };
}
