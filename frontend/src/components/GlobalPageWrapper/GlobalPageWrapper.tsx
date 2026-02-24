import styles from "./GlobalPageWrapper.module.css";

const GlobalPageWrapper = ({ children }: { children: React.ReactNode }) => {
  return <div className={styles.container}>{children}</div>;
};

export default GlobalPageWrapper;
