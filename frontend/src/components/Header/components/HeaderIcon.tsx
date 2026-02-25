import { Link } from "react-router-dom";
import HomeIcon from "../../../assets/icon/header/HomeIcon";
import BasketIcon from "../../../assets/icon/header/BasketIcon";
import styles from "../Header.module.css";

interface HeaderIconProps {
  variant: "basket" | "chat";
}

const HeaderIcon = ({ variant }: HeaderIconProps) => {
  switch (variant) {
    case "chat":
      return (
        <Link to="/basket" className={styles.basketLink}>
          <BasketIcon />
        </Link>
      );

    case "basket":
      return (
        <Link to="/" className={styles.basketLink}>
          <HomeIcon />
        </Link>
      );

    default:
      return null;
  }
};

export default HeaderIcon;
