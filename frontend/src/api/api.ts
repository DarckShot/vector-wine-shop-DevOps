import axios from "axios";
import type {
  UUID,
  Wine,
  SearchWinesRequest,
  SearchWinesResponse,
  GetCartWinesResponse,
  AddWineToCartResponse,
  UpdateCartWineCountRequest,
  UpdateCartWineCountResponse,
  DeleteWineFromCartResponse,
} from "./api.types";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "http://localhost:3000",
});

const MOCK_WINES: Wine[] = [
  {
    id: "11111111-1111-1111-1111-111111111111",
    name: "Riesling Classic",
    description: "Белое вино с цитрусовыми нотами.",
    price: 1299.99,
    color: "white",
    acidity: "dry",
    country: "Germany",
  },
  {
    id: "22222222-2222-2222-2222-222222222222",
    name: "Merlot Reserve",
    description:
      "Красное вино с ягодным профилем. Красное вино с ягодным профилем. Красное вино с ягодным профилем. Красное вино с ягодным профилем. Красное вино с ягодным профилем. Красное вино с ягодным профилем. Красное вино с ягодным профилем. Красное вино с ягодным профилем. ",
    price: 1890,
    color: "red",
    acidity: "semi-dry",
    country: "France",
  },
];

// POST /search/wines
export const searchWines = async (
  payload: SearchWinesRequest,
): Promise<SearchWinesResponse> => {
  // const { data } = await api.post<SearchWinesResponse>("/search/wines", payload);
  // return data;

  console.log("searchWines", payload);

  const returnWines = MOCK_WINES.filter(
    (w) => w.price >= payload.priceMin && w.price <= payload.priceMax,
  );

  return {
    summary: `Мок: результаты по запросу "${payload.query}"`,
    wines: returnWines,
  };
};

// POST /cart/wines/:wine_id
export const addWineToCart = async (
  wineId: UUID,
): Promise<AddWineToCartResponse> => {
  // await api.post<void>(`/cart/wines/${wineId}`);

  console.log("addWineToCart", wineId);

  return;
};

// GET /cart/wines
export const getCartWines = async (): Promise<GetCartWinesResponse> => {
  // console.log("getCartWines");
  // return { wines: MOCK_CART };

  const { data } = await api.get<GetCartWinesResponse>("/cart/wines");
  return data;
};

// PUT /cart/wines/:wine_id
export const updateCartWineCount = async (
  wineId: UUID,
  payload: UpdateCartWineCountRequest,
): Promise<UpdateCartWineCountResponse> => {
  // const { data } = await api.put<UpdateCartWineCountResponse>(`/cart/wines/${wineId}`, payload);
  // return data;

  console.log("updateCartWineCount", wineId, payload);

  return { updatedCount: payload.count };
};

// DELETE /cart/wines/:wine_id
export const deleteWineFromCart = async (
  wineId: UUID,
): Promise<DeleteWineFromCartResponse> => {
  // await api.delete<void>(`/cart/wines/${wineId}`);

  console.log("deleteWineFromCart", wineId);

  return;
};
