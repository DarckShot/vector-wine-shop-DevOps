import { useCallback, useEffect, useRef, useState } from "react";
import type { CartWine } from "../../../api/api.types";
import {
  getCartWines,
  updateCartWineCount,
  deleteWineFromCart,
} from "../../../api/api";

export function useCart() {
  const [wines, setWines] = useState<CartWine[]>([]);
  const [loading, setLoading] = useState(false);

  const winesRef = useRef<CartWine[]>([]);

  const setWinesAndRef = useCallback(
    (updater: CartWine[] | ((prev: CartWine[]) => CartWine[])) => {
      setWines((prev) => {
        const next =
          typeof updater === "function"
            ? (updater as (p: CartWine[]) => CartWine[])(prev)
            : updater;
        winesRef.current = next;
        return next;
      });
    },
    [],
  );

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await getCartWines();
      setWinesAndRef(res.wines ?? []);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const increase = useCallback(
    async (id: string) => {
      const currentCount =
        winesRef.current.find((w) => w.id === id)?.count ?? 0;
      const nextCount = currentCount + 1;

      setWinesAndRef((prev) =>
        prev.map((w) => (w.id === id ? { ...w, count: w.count + 1 } : w)),
      );

      try {
        const res = await updateCartWineCount(id, { count: nextCount });
        if (res?.updatedCount != null) {
          setWinesAndRef((prev) =>
            prev.map((w) =>
              w.id === id ? { ...w, count: res.updatedCount } : w,
            ),
          );
        }
      } catch (err) {
        setWinesAndRef((prev) =>
          prev.map((w) =>
            w.id === id ? { ...w, count: Math.max(0, w.count - 1) } : w,
          ),
        );
        throw err;
      }
    },
    [setWinesAndRef],
  );

  const decrease = useCallback(
    async (id: string) => {
      const currentCount =
        winesRef.current.find((w) => w.id === id)?.count ?? 0;
      const next = Math.max(0, currentCount - 1);

      setWinesAndRef((prev) =>
        prev
          .map((w) =>
            w.id === id ? { ...w, count: Math.max(0, w.count - 1) } : w,
          )
          .filter((w) => w.count > 0),
      );

      try {
        const res = await updateCartWineCount(id, { count: next });
        if (res?.updatedCount != null) {
          if (res.updatedCount <= 0) {
            setWinesAndRef((prev) => prev.filter((w) => w.id !== id));
          } else {
            setWinesAndRef((prev) =>
              prev.map((w) =>
                w.id === id ? { ...w, count: res.updatedCount } : w,
              ),
            );
          }
        }
      } catch (err) {
        load();
        throw err;
      }
    },
    [setWinesAndRef, load],
  );

  const remove = useCallback(
    async (id: string) => {
      const previous = winesRef.current;
      setWinesAndRef((prev) => prev.filter((w) => w.id !== id));
      try {
        await deleteWineFromCart(id);
      } catch (err) {
        setWinesAndRef(previous);
        throw err;
      }
    },
    [setWinesAndRef],
  );

  return {
    wines,
    loading,
    reload: load,
    increase,
    decrease,
    remove,
  } as const;
}
