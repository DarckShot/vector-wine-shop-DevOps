import { useCallback, useEffect, useRef, useState } from "react";
import type { ChatMessage } from "../types";
import { searchWines } from "../../../api/api";

export type UseChatReturn = {
  messages: ChatMessage[];
  value: string;
  setValue: (v: string) => void;
  minPrice: string;
  setMinPrice: (v: string) => void;
  maxPrice: string;
  setMaxPrice: (v: string) => void;
  loading: boolean;
  send: () => Promise<void>;
};

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [value, setValue] = useState("");
  const [minPrice, setMinPrice] = useState("0");
  const [maxPrice, setMaxPrice] = useState("");
  const [loading, setLoading] = useState(false);

  const valueRef = useRef(value);
  const minRef = useRef(minPrice);
  const maxRef = useRef(maxPrice);

  useEffect(() => {
    valueRef.current = value;
  }, [value]);
  useEffect(() => {
    minRef.current = minPrice;
  }, [minPrice]);
  useEffect(() => {
    maxRef.current = maxPrice;
  }, [maxPrice]);

  const send = useCallback(async () => {
    const text = (valueRef.current ?? "").trim();
    if (!text) return;

    const userMsg: ChatMessage = {
      id: String(Date.now()),
      role: "user",
      text,
    };

    setMessages((m) => [...m, userMsg]);
    setValue("");

    setLoading(true);
    try {
      const priceMin = minRef.current ? Number(minRef.current) : 0;
      const priceMax = maxRef.current ? Number(maxRef.current) : 1000000000;

      const payload = {
        query: userMsg.text,
        priceMin,
        priceMax,
      };

      const res = await searchWines(payload);

      const botMsg: ChatMessage = {
        id: String(Date.now() + 1),
        role: "bot",
        text: res.summary,
        wines: res.wines,
      };
      setMessages((m) => [...m, botMsg]);
    } catch (err) {
      const botMsg: ChatMessage = {
        id: String(Date.now() + 2),
        role: "bot",
        text: "Ошибка запроса. Попробуйте ещё раз.",
      };
      setMessages((m) => [...m, botMsg]);
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    messages,
    value,
    setValue,
    minPrice,
    setMinPrice,
    maxPrice,
    setMaxPrice,
    loading,
    send,
  };
}
