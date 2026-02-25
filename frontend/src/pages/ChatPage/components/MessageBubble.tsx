import { memo } from "react";
import type { ChatMessage } from "../types";
import styles from "../ChatPage.module.css";
import WineCard from "./WineCard";

export type MessageBubbleProps = {
  msg: ChatMessage;
  onAdd?: (id: string) => void;
};

const MessageBubble = ({ msg, onAdd }: MessageBubbleProps) => {
  const isUser = msg.role === "user";

  return (
    <div className={isUser ? styles.msgUser : styles.msgBot}>
      <div className={styles.msgBubble}>{msg.text}</div>

      {msg.wines && msg.wines.length > 0 && (
        <div className={styles.wineList}>
          {msg.wines.map((w) => (
            <WineCard key={w.id} wine={w} onAdd={onAdd} />
          ))}
        </div>
      )}
    </div>
  );
};

export default memo(MessageBubble);
