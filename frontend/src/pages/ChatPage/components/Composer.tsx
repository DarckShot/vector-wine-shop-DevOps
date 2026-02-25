import styles from "../ChatPage.module.css";
import { getFieldClass } from "../utils/composerUtils";
import { useComposer } from "../hooks/useComposer";
import { memo, type KeyboardEvent } from "react";

export type ComposerProps = {
  value: string;
  setValue: (v: string) => void;
  minPrice: string;
  setMinPrice: (v: string) => void;
  maxPrice: string;
  setMaxPrice: (v: string) => void;
  loading: boolean;
  onSend: () => void;
  onKeyDown: (e: KeyboardEvent<HTMLTextAreaElement>) => void;
};

const Composer = ({
  value,
  setValue,
  minPrice,
  setMinPrice,
  maxPrice,
  setMaxPrice,
  loading,
  onSend,
  onKeyDown,
}: ComposerProps) => {
  const {
    errors,
    shakes,
    submittedOnce,
    handleSend,
    onValueChange,
    onMinChange,
    onMaxChange,
  } = useComposer({
    value,
    setValue,
    minPrice,
    setMinPrice,
    maxPrice,
    setMaxPrice,
    onSend,
  });

  return (
    <div className={styles.composer}>
      <textarea
        placeholder="Какое винишко выпьем сегодня? (Enter — отправить, Shift+Enter — новая строка)"
        value={value}
        onChange={onValueChange}
        onKeyDown={onKeyDown}
        className={getFieldClass(
          styles.textarea,
          errors.value || (submittedOnce && value.trim() === ""),
          shakes.value,
          styles.inputError,
          styles.shake,
        )}
        aria-label="Сообщение"
        rows={4}
        aria-multiline="true"
      />

      <div className={styles.priceColumn}>
        <input
          type="number"
          placeholder="Мин. цена"
          className={getFieldClass(
            styles.priceInput,
            errors.minPrice ||
              (submittedOnce && String(minPrice).trim() === ""),
            shakes.minPrice,
            styles.inputError,
            styles.shake,
          )}
          value={minPrice}
          onChange={onMinChange}
          aria-label="Минимальная цена"
          name="minPrice"
        />
        <input
          type="number"
          placeholder="Макс. цена"
          className={getFieldClass(
            styles.priceInput,
            errors.maxPrice ||
              (submittedOnce && String(maxPrice).trim() === ""),
            shakes.maxPrice,
            styles.inputError,
            styles.shake,
          )}
          value={maxPrice}
          onChange={onMaxChange}
          aria-label="Максимальная цена"
          name="maxPrice"
        />
      </div>

      <button
        onClick={handleSend}
        className={styles.sendBtn}
        disabled={loading}
        aria-label="Отправить сообщение"
      >
        Отправить
      </button>
    </div>
  );
};

export default memo(Composer);
