import { Routes, Route } from "react-router-dom";
import Header from "./components/Header.jsx";
import Home from "./pages/Home.jsx";
import CafePoint from "./pages/CafePoint.jsx";

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home />} />
          {/* :id тут — це slug закладу (напр. "cafe-1"), а не числовий id з БД */}
          <Route path="/point/:id" element={<CafePoint />} />
        </Routes>
      </main>
    </div>
  );
}
