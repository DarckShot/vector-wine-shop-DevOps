export function formatPrice(value: number): string {
  if (Number.isNaN(value) || !Number.isFinite(value)) return "— ₽";
  return Math.round(value).toLocaleString("ru-RU") + " ₽";
}
