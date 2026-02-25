import { memo, useCallback } from "react";
import type { Wine } from "../../../api/api.types";
import styles from "../ChatPage.module.css";
import { formatPrice } from "../utils/formatPrice";

interface WineCardProps {
  wine: Wine;
  onAdd?: (id: string) => void;
}

const WineCard = ({ wine, onAdd }: WineCardProps) => {
  const handleAdd = useCallback(() => {
    onAdd?.(wine.id);
  }, [onAdd, wine.id]);

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
        <div className={styles.winePrice}>
          {formatPrice(Number(wine.price))}
        </div>
        <button
          className={styles.addBtn}
          onClick={handleAdd}
          aria-label={`Добавить ${wine.name}`}
        >
          Добавить
        </button>
      </div>
    </div>
  );
};

export default memo(WineCard);
