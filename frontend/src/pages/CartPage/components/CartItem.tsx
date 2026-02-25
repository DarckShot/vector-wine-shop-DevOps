import { memo, useCallback } from "react";
import type { CartWine } from "../../../api/api.types";
import styles from "../../ChatPage/ChatPage.module.css";
import { formatPrice } from "../../ChatPage/utils/formatPrice";

type CartItemProps = {
  wine: CartWine;
  onIncrease: (id: string) => void;
  onDecrease: (id: string) => void;
  onRemove: (id: string) => void;
};

const CartItem = ({
  wine,
  onIncrease,
  onDecrease,
  onRemove,
}: CartItemProps) => {
  const handleDecrease = useCallback(() => {
    onDecrease(wine.id);
  }, [onDecrease, wine.id]);

  const handleIncrease = useCallback(() => {
    onIncrease(wine.id);
  }, [onIncrease, wine.id]);

  const handleRemove = useCallback(() => {
    onRemove(wine.id);
  }, [onRemove, wine.id]);

  return (
    <div className={styles.wineCard}>
      <div className={styles.wineInfo}>
        <div className={styles.wineName}>{wine.name}</div>
        <div className={styles.wineMeta}>
          {wine.country} • {wine.color} • {wine.acidity}
        </div>
        {wine.description && (
          <div className={styles.wineDescriptionWrap}>
            <div className={styles.wineDescription}>{wine.description}</div>
          </div>
        )}
      </div>

      <div className={styles.wineActions}>
        <div>
          <div className={styles.winePrice}>
            {formatPrice(Number(wine.price))}
          </div>
          <div className={styles.controls}>
            <button
              className={styles.addBtn}
              onClick={handleDecrease}
              aria-label={`Уменьшить ${wine.name}`}
            >
              –
            </button>
            <div className={styles.countBadge}>{wine.count}</div>
            <button
              className={styles.addBtn}
              onClick={handleIncrease}
              aria-label={`Увеличить ${wine.name}`}
            >
              +
            </button>
          </div>
        </div>

        <button
          className={styles.addBtn}
          onClick={handleRemove}
          aria-label={`Удалить ${wine.name}`}
        >
          Удалить
        </button>
      </div>
    </div>
  );
};

export default memo(CartItem);
