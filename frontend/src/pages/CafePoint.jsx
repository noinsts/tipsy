import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { getShiftBySlug, ApiError } from "../api.js";
import LoadingState from "../components/LoadingState.jsx";
import ErrorState from "../components/ErrorState.jsx";
import BaristaCard from "../components/BaristaCard.jsx";

export default function CafePoint() {
  const { id: slug } = useParams();

  const [cafeName, setCafeName] = useState("");
  const [baristas, setBaristas] = useState([]);
  const [noShiftToday, setNoShiftToday] = useState(false);
  const [notFound, setNotFound] = useState(false);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    setNotFound(false);
    setNoShiftToday(false);

    getShiftBySlug(slug)
        .then((data) => {
          setCafeName(data.cafeName);
          if (data.baristas && data.baristas.length > 0) {
            setBaristas(data.baristas);
          } else {
            setNoShiftToday(true);
          }
        })
        .catch((err) => {
          if (err instanceof ApiError && (err.code === "CAFE_NOT_FOUND" || err.code === "SHIFT_NOT_FOUND")) {
            setNotFound(true);
          } else {
            setError(err.message || "Не вдалося завантажити дані");
          }
        })
        .finally(() => setLoading(false));
  }, [slug]);

  useEffect(() => {
    load();
  }, [load]);

  if (loading) return <LoadingState label="Дивимось, хто сьогодні на зміні..." />;
  if (error) return <ErrorState message={error} onRetry={load} />;

  if (notFound) {
    return (
        <div className="max-w-2xl mx-auto px-6 py-16 text-center">
          <p className="text-ink/70 mb-4">Такого закладу немає або зміну не знайдено.</p>
          <Link to="/" className="text-sage hover:text-sageDark underline">
            Повернутися до списку
          </Link>
        </div>
    );
  }

  return (
      <div className="max-w-2xl mx-auto px-6 py-14">
        <Link to="/" className="text-sm text-ink/50 hover:text-sage transition-colors">
          ← Усі заклади
        </Link>

        <h1 className="font-display text-4xl text-espresso mt-4 mb-12">{cafeName}</h1>

        {noShiftToday ? (
            <div className="text-center py-10 border border-dashed border-espresso/20 rounded-2xl">
              <p className="text-ink/60">
                Сьогодні тут ще ніхто не заступив на зміну.
                <br />
                Спробуй зайти трохи пізніше.
              </p>
            </div>
        ) : (
            <div className="grid gap-8 sm:grid-cols-1 md:grid-cols-2 justify-center">
              {baristas.map((barista, index) => (
                  <BaristaCard key={barista.name + index} barista={barista} />
              ))}
            </div>
        )}
      </div>
  );
}