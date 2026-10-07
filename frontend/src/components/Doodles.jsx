/* SVG-фільтр, що робить краї плям нерівними, як акварель. Рендериться один раз. */
export function SketchDefs() {
  return (
    <svg width="0" height="0" className="absolute" aria-hidden="true" focusable="false">
      <defs>
        <filter id="rough" x="-10%" y="-10%" width="120%" height="120%">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" result="noise" />
          <feDisplacementMap in="SourceGraphic" in2="noise" scale="9" />
        </filter>
      </defs>
    </svg>
  );
}

/* Акварельна пляма з нерівним краєм */
export function Blob({ className = "" }) {
  return (
    <div
      aria-hidden="true"
      className={`absolute inset-0 ${className}`}
      style={{ filter: "url(#rough)" }}
    />
  );
}

export function Heart({ className = "" }) {
  return (
    <svg
      viewBox="0 0 40 40"
      className={`w-6 h-6 text-accentDark ${className}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="3"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M20 34 C6 24 4 14 11 9 C16 6 19 10 20 13 C21 10 24 6 29 9 C36 14 34 24 20 34 Z" />
    </svg>
  );
}

/* Три короткі штрихи — "іскри" навколо заголовків */
export function Sparks({ className = "", flip = false }) {
  return (
    <svg
      viewBox="0 0 40 40"
      className={`w-8 h-8 text-sketch ${className}`}
      style={flip ? { transform: "scaleX(-1)" } : undefined}
      fill="none"
      stroke="currentColor"
      strokeWidth="2.6"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M6 22 L17 18" />
      <path d="M12 8 L20 15" />
      <path d="M27 4 L28 15" />
    </svg>
  );
}

/* Хвиляста лінія-підкреслення на всю ширину батьківського елемента */
export function Underline({ className = "" }) {
  return (
    <svg
      viewBox="0 0 200 8"
      preserveAspectRatio="none"
      className={`block w-full h-2 text-sketch ${className}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2.5"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M2 5 C40 1 80 7 120 3 S180 3 198 2" />
    </svg>
  );
}

/* Хвиляста лінія між секціями */
export function WaveDivider() {
  return (
    <svg
      viewBox="0 0 1000 24"
      preserveAspectRatio="none"
      className="block w-full h-6 text-sketch/70"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      aria-hidden="true"
    >
      <path d="M0 18 C150 4 300 8 450 14 S800 20 1000 6" />
    </svg>
  );
}

/* Усміхнена чашка з парою — "аватар" бариста без фото */
export function CupFace({ className = "" }) {
  return (
    <svg
      viewBox="0 0 64 64"
      className={`w-14 h-14 text-pen ${className}`}
      fill="none"
      stroke="currentColor"
      strokeWidth="2.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d="M24 6 C21 10 27 12 24 17" />
      <path d="M33 8 C31 11 35 13 33 16" />
      <path d="M11 24 H49 V36 A19 19 0 0 1 30 55 A19 19 0 0 1 11 36 Z" />
      <path d="M49 28 H53 A6.5 6.5 0 0 1 53 41 H47" />
      <circle cx="23" cy="35" r="1.3" fill="currentColor" />
      <circle cx="35" cy="35" r="1.3" fill="currentColor" />
      <path d="M25 42 Q29 46 33 42" />
    </svg>
  );
}
