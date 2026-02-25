import type { ReactNode } from "react";
import styles from "./GlobalPageWrapper.module.css";

const GlobalPageWrapper = ({ children }: { children: ReactNode }) => {
  return <div className={styles.container}>{children}</div>;
};

export default GlobalPageWrapper;
