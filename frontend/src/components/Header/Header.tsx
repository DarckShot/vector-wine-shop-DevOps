import HeaderIcon from "./components/HeaderIcon";
import styles from "./Header.module.css";

interface HeaderProps {
  title: string;
  variant?: "basket" | "chat";
}

const Header = ({ title, variant = "basket" }: HeaderProps) => {
  return (
    <header className={styles.header}>
      <h1 className={styles.headerTitle}>{title}</h1>
      <HeaderIcon variant={variant} />
    </header>
  );
};

export default Header;
