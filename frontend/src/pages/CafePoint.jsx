import { useEffect, useState, useCallback } from "react";
import { useParams, Link } from "react-router-dom";
import { getShiftBySlug, ApiError } from "../api.js";
import LoadingState from "../components/LoadingState.jsx";
import ErrorState from "../components/ErrorState.jsx";
import BaristaCard from "../components/BaristaCard.jsx";
import { Blob, CupFace, Heart, SketchDefs, Sparks, Underline, WaveDivider } from "../components/Doodles.jsx";

// Тексти, що залежать від типу закладу. Змінюй вільно.
const THEMES = {
  zona: { theme: "blue", tagline: "Смачна кава і хороші люди", role: "Бариста" },
  doner: { theme: "green", tagline: "Свіжий донер і хороші люди", role: "Бариста" },
};

// "Zona Coffee Яготин" -> бренд "Zona Coffee" + місце "Яготин".
// Якщо API віддає data.cafe.city — використається воно.
function splitName(name, city) {
  const words = (name || "").trim().split(/\s+/);
  if (city) return [name, city];
  return [words.slice(0, 2).join(" "), words.slice(2).join(" ")];
}

export default function CafePoint() {
  const { id: slug } = useParams();

  const [cafeName, setCafeName] = useState("");
  const [cafeCity, setCafeCity] = useState("");
  const [cafeDescription, setCafeDescription] = useState("");
  const [cafePhotoUrl, setCafePhotoUrl] = useState("");
  const [cafeType, setCafeType] = useState("");
  const [baristas, setBaristas] = useState([]);
  const [jarUrl, setJarUrl] = useState("");
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
        if (data?.cafe) {
          setCafeName(data.cafe.name);
          setCafeCity(data.cafe.city ?? "");
          setCafeDescription(data.cafe.description);
          setCafePhotoUrl(data.cafe.photoUrl);
          setCafeType(data.cafe.type); // zona / doner
        }
        setJarUrl(data.jarUrl);
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

  // Перемикаємо кольорову тему на всій сторінці (разом із шапкою і тлом)
  const cfg = THEMES[cafeType] ?? THEMES.zona;
  useEffect(() => {
    document.documentElement.dataset.theme = cfg.theme;
    return () => {
      delete document.documentElement.dataset.theme;
    };
  }, [cfg.theme]);

  if (loading) return <LoadingState label="Дивимось, хто сьогодні на зміні..." />;
  if (error) return <ErrorState message={error} onRetry={load} />;

  if (notFound) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-24 text-center">
        <p className="text-pen/70 mb-4">Такого закладу немає або зміну не знайдено.</p>
        <Link to="/" className="text-accentDark underline underline-offset-4 hover:text-accent">
          Повернутися до списку
        </Link>
      </div>
    );
  }

  const [brand, place] = splitName(cafeName, cafeCity);

  return (
    <div className="pb-20">
      <SketchDefs />

      {/* ───── Hero ───── */}
      <section className="max-w-4xl mx-auto px-6 pt-8">
        <Link to="/" className="text-sm text-pen/50 hover:text-accentDark transition-colors">
          ← Усі заклади
        </Link>

        <div className="mt-6 grid gap-10 md:grid-cols-2 md:items-center">
          <div>
            <div className="relative inline-block -rotate-6 mb-6">
              <p className="font-hand text-2xl md:text-3xl leading-tight text-pen/80 max-w-[11rem]">
                {cfg.tagline}
              </p>
              <Underline className="mt-1" />
              <Heart className="absolute -right-12 -top-1 w-9 h-9 rotate-6" />
              <Sparks className="absolute -right-20 top-0 w-7 h-7" />
            </div>

            <h1 className="font-brush uppercase text-6xl md:text-7xl leading-[0.95] text-pen -rotate-2 origin-left">
              {brand}
            </h1>
            {place && (
              <p className="font-hand text-5xl md:text-6xl font-semibold text-pen/70 mt-2 ml-2">{place}</p>
            )}

            {cafeDescription && (
              <p className="relative mt-8 max-w-xs text-pen/70 leading-relaxed">
                {cafeDescription}
                <Heart className="absolute -right-8 top-5 w-5 h-5 rotate-12" />
              </p>
            )}
          </div>

          <div className="relative aspect-[4/5] md:aspect-square">
            <Blob className="bg-sketch/30 rounded-[40%_60%_55%_45%/50%_40%_60%_50%] scale-105" />
            {cafePhotoUrl ? (
              <img
                src={cafePhotoUrl}
                alt={cafeName}
                className="relative w-full h-full object-cover rounded-[2rem]"
                style={{ filter: "url(#rough)" }}
              />
            ) : (
              <div className="relative w-full h-full flex items-center justify-center">
                <CupFace className="w-40 h-40" />
              </div>
            )}
            <Sparks className="absolute -right-2 bottom-2 w-8 h-8" />
          </div>
        </div>
      </section>

      <div className="max-w-4xl mx-auto px-6 mt-14">
        <WaveDivider />
      </div>

      {/* ───── Хто на зміні ───── */}
      <section className="max-w-4xl mx-auto px-6 mt-14 text-center">
        <div className="inline-flex items-center gap-3">
          <Sparks className="-rotate-12" />
          <div>
            <h2 className="font-hand text-5xl font-semibold text-pen">Хто на зміні?</h2>
            <Underline className="mt-1 text-accent" />
          </div>
          <Sparks flip className="rotate-12" />
        </div>

        {noShiftToday ? (
          <div className="relative mt-12 mx-auto max-w-md px-8 py-10">
            <Blob className="border-2 border-dashed border-sketch/60 rounded-[2.5rem]" />
            <p className="relative text-pen/60">
              Сьогодні тут ще ніхто не заступив на зміну.
              <br />
              Спробуй зайти трохи пізніше.
            </p>
          </div>
        ) : (
          <>
            <div className="mt-12 flex flex-wrap justify-center gap-8">
              {baristas.map((barista, index) => (
                <BaristaCard key={barista.name + index} barista={barista} />
              ))}
            </div>

            {/* ───── Чайові ───── */}
            <div className="mt-16 flex flex-col items-center">
              <div className="mb-5">
                <p className="font-hand text-2xl text-pen/80">Підтримай команду</p>
                <Underline className="mt-0.5" />
              </div>

              {jarUrl ? (
                <div className="relative">
                  <Sparks className="absolute -left-12 top-1 w-9 h-9 -rotate-12" />
                  <a
                    href={jarUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-3 px-9 py-4 rounded-full bg-accent text-white text-lg font-medium hover:bg-accentDark transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-accentDark"
                  >
                    <CupFace className="w-7 h-7 text-white" />
                    Залишити чайові
                    <span aria-hidden="true">→</span>
                  </a>
                  <Sparks flip className="absolute -right-12 top-1 w-9 h-9 rotate-12" />
                </div>
              ) : (
                <p className="text-pen/50 text-sm">Банку для чайових ще не додано</p>
              )}
            </div>
          </>
        )}
      </section>
    </div>
  );
}
