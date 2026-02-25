import Header from "../../components/Header/Header";
import { useCart } from "./hooks/useCart";
import CartItem from "./components/CartItem";
import styles from "../ChatPage/ChatPage.module.css";

const CartPage = () => {
  const { wines, loading, increase, decrease, remove } = useCart();

  return (
    <main>
      <Header title="Корзина" variant="basket" />

      <section className={styles.pageSection}>
        {loading && <div>Загрузка...</div>}

        {!loading && wines.length === 0 && <div>Корзина пуста</div>}
        <div className={styles.cartGrid}>
          {wines.map((w) => (
            <CartItem
              key={w.id}
              wine={w}
              onIncrease={increase}
              onDecrease={decrease}
              onRemove={remove}
            />
          ))}
        </div>
      </section>
    </main>
  );
};

export default CartPage;
