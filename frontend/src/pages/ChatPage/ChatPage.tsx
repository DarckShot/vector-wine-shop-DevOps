import {
  useEffect,
  useRef,
  useMemo,
  useCallback,
  type KeyboardEvent,
} from "react";
import Header from "../../components/Header/Header";
import styles from "./ChatPage.module.css";
import { useChat } from "./hooks/useChat";
import MessageBubble from "./components/MessageBubble";
import Composer from "./components/Composer";
import { addWineToCart } from "../../api/api";

const Chat = () => {
  const {
    messages,
    value,
    setValue,
    minPrice,
    setMinPrice,
    maxPrice,
    setMaxPrice,
    loading,
    send,
  } = useChat();

  const listRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const el = listRef.current;
    if (!el) return;
    el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
  }, [messages.length, loading]);

  const onKeyDown = useCallback(
    (e: KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        send();
      }
    },
    [send],
  );

  const onSend = useCallback(() => {
    send();
  }, [send]);

  const onAdd = useCallback(
    (id: string) => {
      addWineToCart(id);
    },
    [addWineToCart],
  );

  const messageElements = useMemo(
    () =>
      messages.map((m) => <MessageBubble key={m.id} msg={m} onAdd={onAdd} />),
    [messages, onAdd],
  );

  return (
    <main className={styles.page}>
      <Header title="Чат" variant="chat" />

      <section className={styles.chatWrap}>
        <div className={styles.container}>
          <div className={styles.messages} ref={listRef}>
            {messageElements}

            {loading && (
              <div className={styles.msgBot}>
                <div className={styles.msgBubble}>Отправка...</div>
              </div>
            )}
          </div>

          <Composer
            value={value}
            setValue={setValue}
            minPrice={minPrice}
            setMinPrice={setMinPrice}
            maxPrice={maxPrice}
            setMaxPrice={setMaxPrice}
            loading={loading}
            onSend={onSend}
            onKeyDown={onKeyDown}
          />
        </div>
      </section>
    </main>
  );
};

export default Chat;
