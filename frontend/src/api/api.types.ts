export type UUID = string;

export type WineColor = "red" | "white";
export type WineAcidity = "dry" | "semi-dry" | "semi-sweet" | "sweet";

export type Wine = {
  id: UUID;
  name: string;
  price: number;
  description?: string;
  color?: WineColor;
  acidity?: WineAcidity;
  country?: string;
};

export type CartWine = Wine & {
  count: number;
};

// ----- /search/wines -----
export type SearchWinesRequest = {
  query: string;
  priceMin: number;
  priceMax: number;
};

export type SearchWinesResponse = {
  summary: string;
  wines: Wine[];
};

// ----- /cart/wines -----
export type GetCartWinesResponse = {
  wines: CartWine[];
};

// POST /cart/wines/:wine_id
export type AddWineToCartResponse = void;

// PUT /cart/wines/:wine_id
export type UpdateCartWineCountRequest = {
  count: number;
};

export type UpdateCartWineCountResponse = {
  updatedCount: number;
};

// DELETE /cart/wines/:wine_id -> 204
export type DeleteWineFromCartResponse = void;
