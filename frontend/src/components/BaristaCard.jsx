import { useMemo } from "react";
import { Blob, CupFace, Heart, Sparks, Underline } from "./Doodles.jsx";

/* Чи сьогодні день народження? Підтримує "YYYY-MM-DD", ISO-рядок, "DD.MM.YYYY" і Date.
   Для рядків беремо місяць/день прямо з тексту, щоб часові пояси не зсунули дату. */
function isBirthdayToday(value) {
  if (!value) return false;

  let month, day;
  if (typeof value === "string") {
    let m = value.match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (m) {
      month = +m[2];
      day = +m[3];
    } else if ((m = value.match(/^(\d{1,2})\.(\d{1,2})\.(\d{4})/))) {
      day = +m[1];
      month = +m[2];
    }
  }
  if (!month) {
    const d = new Date(value);
    if (Number.isNaN(d.getTime())) return false;
    month = d.getMonth() + 1;
    day = d.getDate();
  }

  const now = new Date();
  const tm = now.getMonth() + 1;
  const td = now.getDate();
  if (month === tm && day === td) return true;

  // Народжені 29 лютого у невисокосний рік — вітаємо 28-го
  const leap = new Date(now.getFullYear(), 1, 29).getMonth() === 1;
  return month === 2 && day === 29 && !leap && tm === 2 && td === 28;
}

const CONFETTI_COLORS = ["#f472b6", "#fbbf24", "#34d399", "#60a5fa", "#a78bfa", "#fb7185", "#f97316"];

const BIRTHDAY_CSS = `
@keyframes bday-fall {
  0%   { top: -12%; opacity: 0; transform: translateX(0) rotate(0deg); }
  10%  { opacity: 1; }
  50%  { transform: translateX(var(--sway)) rotate(180deg); }
  90%  { opacity: 1; }
  100% { top: 105%; opacity: 0; transform: translateX(calc(var(--sway) * -1)) rotate(360deg); }
}
@keyframes bday-twinkle {
  0%, 100% { transform: scale(0.6) rotate(0deg); opacity: 0.4; }
  50%      { transform: scale(1.15) rotate(20deg); opacity: 1; }
}
@keyframes bday-hat {
  0%, 100% { transform: rotate(-18deg); }
  50%      { transform: rotate(-12deg) translateY(-2px); }
}
@keyframes bday-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(251, 191, 36, 0.0); }
  50%      { box-shadow: 0 0 14px 3px rgba(251, 191, 36, 0.65); }
}
.bday-piece   { position: absolute; animation: bday-fall linear infinite; }
.bday-twinkle { animation: bday-twinkle 1.8s ease-in-out infinite; }
.bday-hat     { animation: bday-hat 2.4s ease-in-out infinite; transform-origin: 50% 100%; }
.bday-glow    { animation: bday-glow 2.2s ease-in-out infinite; }
@media (prefers-reduced-motion: reduce) {
  .bday-piece, .bday-twinkle, .bday-hat, .bday-glow { animation: none; }
  .bday-piece { top: 20%; opacity: 0.8; }
}
`;

/* Конфеті, що падає всередині картки. Позиції детерміновані — не "стрибають" при рендері. */
function Confetti() {
  const pieces = useMemo(
    () =>
      Array.from({ length: 22 }, (_, i) => ({
        left: (i * 37 + 11) % 96,
        delay: -((i * 0.47) % 4.5),
        duration: 3.2 + ((i * 13) % 20) / 10,
        size: 5 + ((i * 7) % 5),
        color: CONFETTI_COLORS[i % CONFETTI_COLORS.length],
        round: i % 3 === 0,
        sway: ((i % 2 ? 1 : -1) * (6 + ((i * 5) % 10))) + "px",
      })),
    []
  );

  return (
    <div
      aria-hidden="true"
      className="absolute inset-0 overflow-hidden rounded-[2.5rem] pointer-events-none"
    >
      {pieces.map((p, i) => (
        <span
          key={i}
          className="bday-piece"
          style={{
            left: `${p.left}%`,
            width: p.size,
            height: p.round ? p.size : p.size * 1.7,
            background: p.color,
            borderRadius: p.round ? "9999px" : "2px",
            animationDelay: `${p.delay}s`,
            animationDuration: `${p.duration}s`,
            "--sway": p.sway,
          }}
        />
      ))}
    </div>
  );
}

/* Святковий ковпачок на аватарці */
function PartyHat({ className = "" }) {
  return (
    <svg
      viewBox="0 0 40 44"
      className={`bday-hat w-9 h-10 ${className}`}
      aria-hidden="true"
    >
      <path d="M20 6 L33 40 H7 Z" fill="#f472b6" stroke="#be185d" strokeWidth="2" strokeLinejoin="round" />
      <path d="M14 26 L27 22" stroke="#fde68a" strokeWidth="3" strokeLinecap="round" />
      <path d="M11 34 L30 29" stroke="#fde68a" strokeWidth="3" strokeLinecap="round" />
      <circle cx="20" cy="6" r="4" fill="#fbbf24" stroke="#b45309" strokeWidth="1.5" />
    </svg>
  );
}

export default function BaristaCard({ barista }) {
  const { name, photoUrl, birthdayDate } = barista;
  const birthday = isBirthdayToday(birthdayDate);

  return (
    <div className="relative px-6 py-5 min-w-[15rem]">
      {birthday && <style>{BIRTHDAY_CSS}</style>}

      <Blob className="bg-tint rounded-[2.5rem]" />
      {birthday && <Confetti />}
      <Sparks className="absolute -left-3 top-0 w-7 h-7 -rotate-12" />

      {birthday && (
        <>
          <Sparks
            flip
            className="bday-twinkle absolute -right-3 -top-2 w-8 h-8 rotate-12 !text-amber-400"
          />
          <Sparks
            className="bday-twinkle absolute -right-2 -bottom-2 w-6 h-6 !text-pink-400"
          />
        </>
      )}

      <div className="relative flex items-center gap-4">
        <div className="relative shrink-0">
          {photoUrl ? (
            <img
              src={photoUrl}
              alt={name}
              className={`w-16 h-16 rounded-full object-cover ring-2 ${
                birthday ? "ring-amber-400 bday-glow" : "ring-pen/80"
              }`}
            />
          ) : (
            <CupFace className={birthday ? "bday-glow rounded-full" : ""} />
          )}
          {birthday && <PartyHat className="absolute -top-6 -left-3" />}
        </div>

        <div className="min-w-0">
          <div className="flex items-start gap-1.5">
            <h3 className="font-hand text-3xl font-semibold leading-none text-pen">{name}</h3>
            <Heart className="w-4 h-4 mt-0.5 shrink-0" />
          </div>
          <Underline className="mt-1 text-pen/80" />
          {birthday ? (
            <p className="font-hand text-xl leading-tight text-accentDark mt-1">
              🎂 З днем народження!
            </p>
          ) : (
            <p className="text-sm text-pen/60 mt-1.5">Бариста</p>
          )}
        </div>
      </div>
    </div>
  );
}
