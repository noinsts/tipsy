import { useEffect, useState, useCallback } from "react";
import { Link } from "react-router-dom";
import { getCafes } from "../api.js";
import LoadingState from "../components/LoadingState.jsx";
import ErrorState from "../components/ErrorState.jsx";

export default function Home() {
  const [cafes, setCafes] = useState(null);
  const [error, setError] = useState(null);

  const load = useCallback(() => {
    setError(null);
    setCafes(null);
    getCafes()
      .then(setCafes)
      .catch((err) => setError(err.message));
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  if (error) return <ErrorState message={error} onRetry={load} />;
  if (!cafes) return <LoadingState label="Завантажуємо список закладів..." />;

  return (
    <div className="max-w-2xl mx-auto px-6 py-14">
      <h1 className="font-display text-4xl text-espresso mb-2">Zone Coffee | Green Donner</h1>
      <p className="text-ink/60 mb-10">Обери заклад, щоб побачити, хто зараз на зміні.</p>

      {cafes.length === 0 ? (
        <p className="text-ink/50">Закладів пока немає.</p>
      ) : (
        <ol className="divide-y divide-espresso/10 border-t border-b border-espresso/10">
          {cafes.map((cafe, index) => (
            <li key={cafe.id}>
              <Link
                to={`/point/${cafe.slug}`}
                className="group flex items-center gap-5 py-5 hover:bg-espresso/[0.03] transition-colors"
              >
                <span className="font-display text-2xl text-gold w-10 shrink-0 text-right">
                  {index + 1}
                </span>
                <span className="flex-1 text-lg text-ink group-hover:text-espresso">
                  {cafe.name}
                </span>
                <svg
                  className="w-5 h-5 text-ink/30 group-hover:text-sage group-hover:translate-x-0.5 transition-all"
                  viewBox="0 0 20 20"
                  fill="none"
                >
                  <path
                    d="M7 4l6 6-6 6"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
              </Link>
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
