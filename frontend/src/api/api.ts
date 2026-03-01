import axios from "axios";
import type {
  UUID,
  SearchWinesRequest,
  SearchWinesResponse,
  GetCartWinesResponse,
  AddWineToCartResponse,
  UpdateCartWineCountRequest,
  UpdateCartWineCountResponse,
  DeleteWineFromCartResponse,
} from "./api.types";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000",
});

// POST /search/wines
export const searchWines = async (
  payload: SearchWinesRequest,
): Promise<SearchWinesResponse> => {
  console.log("searchWines", payload);

  const { data } = await api.post<SearchWinesResponse>(
    "/search/wines",
    payload,
  );

  console.log("response /search/wines", data);

  return data;
};

// POST /cart/wines/:wine_id
export const addWineToCart = async (
  wineId: UUID,
): Promise<AddWineToCartResponse> => {
  console.log("addWineToCart", wineId);

  await api.post<void>(`/cart/wines/${wineId}`);

  console.log("response /cart/wines/${wineId}");

  return;
};

// GET /cart/wines
export const getCartWines = async (): Promise<GetCartWinesResponse> => {
  console.log("getCartWines");

  const { data } = await api.get<GetCartWinesResponse>("/cart/wines");

  console.log("response /cart/wines", data);

  return data;
};

// PUT /cart/wines/:wine_id
export const updateCartWineCount = async (
  wineId: UUID,
  payload: UpdateCartWineCountRequest,
): Promise<UpdateCartWineCountResponse> => {
  console.log("updateCartWineCount", wineId, payload);

  const { data } = await api.put<UpdateCartWineCountResponse>(
    `/cart/wines/${wineId}`,
    payload,
  );

  console.log("response /cart/wines/${wineId}", data);

  return data;
};

// DELETE /cart/wines/:wine_id
export const deleteWineFromCart = async (
  wineId: UUID,
): Promise<DeleteWineFromCartResponse> => {
  console.log("deleteWineFromCart", wineId);

  await api.delete<void>(`/cart/wines/${wineId}`);

  console.log("response /cart/wines/${wineId}");

  return;
};
