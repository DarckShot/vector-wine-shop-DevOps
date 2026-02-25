import "./App.css";
import GlobalPageWrapper from "./components/GlobalPageWrapper/GlobalPageWrapper";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import ChatPage from "./pages/ChatPage/ChatPage";
import CartPage from "./pages/CartPage/CartPage";

function App() {
  return (
    <BrowserRouter>
      <GlobalPageWrapper>
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/basket" element={<CartPage />} />
        </Routes>
      </GlobalPageWrapper>
    </BrowserRouter>
  );
}

export default App;
