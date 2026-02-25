import {
  useCallback,
  useState,
  useEffect,
  useRef,
  type ChangeEvent,
} from "react";
import { isBlank } from "../utils/composerUtils";
import type { FieldState } from "../types";

type UseComposerArgs = {
  value: string;
  setValue: (v: string) => void;
  minPrice: string;
  setMinPrice: (v: string) => void;
  maxPrice: string;
  setMaxPrice: (v: string) => void;
  onSend: () => void;
};

export function useComposer({
  value,
  setValue,
  minPrice,
  setMinPrice,
  maxPrice,
  setMaxPrice,
  onSend,
}: UseComposerArgs) {
  const [errors, setErrors] = useState<FieldState>({
    value: false,
    minPrice: false,
    maxPrice: false,
  });
  const [shakes, setShakes] = useState<FieldState>({
    value: false,
    minPrice: false,
    maxPrice: false,
  });
  const [submittedOnce, setSubmittedOnce] = useState(false);
  const timeoutsRef = useRef<number[]>([]);

  const triggerError = useCallback((field: keyof FieldState) => {
    setErrors((s) => ({ ...s, [field]: true }));
    setShakes((s) => ({ ...s, [field]: true }));
    const id = setTimeout(
      () => setShakes((s) => ({ ...s, [field]: false })),
      600,
    );
    timeoutsRef.current.push(id as unknown as number);
  }, []);

  const handleSend = useCallback(() => {
    setSubmittedOnce(true);

    const missingValue = isBlank(value);
    const missingMin = isBlank(minPrice);
    const missingMax = isBlank(maxPrice);

    let hasError = false;
    if (missingValue) {
      triggerError("value");
      hasError = true;
    }
    if (missingMin) {
      triggerError("minPrice");
      hasError = true;
    }
    if (missingMax) {
      triggerError("maxPrice");
      hasError = true;
    }

    if (hasError) return;

    onSend();

    setSubmittedOnce(false);
    setErrors({ value: false, minPrice: false, maxPrice: false });
    setShakes({ value: false, minPrice: false, maxPrice: false });
  }, [value, minPrice, maxPrice, onSend, triggerError]);

  const onValueChange = useCallback(
    (e: ChangeEvent<HTMLTextAreaElement>) => {
      setValue(e.target.value);
      setErrors((s) => (s.value ? { ...s, value: false } : s));
    },
    [setValue, setErrors],
  );

  const onMinChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      setMinPrice(e.target.value);
      setErrors((s) => (s.minPrice ? { ...s, minPrice: false } : s));
    },
    [setMinPrice, setErrors],
  );

  const onMaxChange = useCallback(
    (e: ChangeEvent<HTMLInputElement>) => {
      setMaxPrice(e.target.value);
      setErrors((s) => (s.maxPrice ? { ...s, maxPrice: false } : s));
    },
    [setMaxPrice, setErrors],
  );

  useEffect(() => {
    return () => {
      timeoutsRef.current.forEach((id) => clearTimeout(id));
      timeoutsRef.current = [];
    };
  }, []);

  return {
    errors,
    shakes,
    submittedOnce,
    triggerError,
    handleSend,
    setErrors,
    onValueChange,
    onMinChange,
    onMaxChange,
  };
}
