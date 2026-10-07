/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        espresso: "#231912",
        ink: "#2A2118",
        paper: "#F2EEE4",
        paperDark: "#E7E0D0",
        sage: "#5C6B4F",
        sageDark: "#48543E",
        gold: "#C9A227",
        canvas: "rgb(var(--canvas) / <alpha-value>)",
        pen: "rgb(var(--pen) / <alpha-value>)",
        accent: "rgb(var(--accent) / <alpha-value>)",
        accentDark: "rgb(var(--accent-dark) / <alpha-value>)",
        tint: "rgb(var(--tint) / <alpha-value>)",
        sketch: "rgb(var(--sketch) / <alpha-value>)",
      },
      fontFamily: {
        display: ["Fraunces", "serif"],
        sans: ["Inter", "sans-serif"],
        brush: ['"Caveat Brush"', "cursive"], // великий заголовок
        hand: ["Caveat", "cursive"],          // підписи від руки
        body: ["Onest", "system-ui", "sans-serif"],
      },
      keyframes: {
        riseIn: {
          "0%": { opacity: "0", transform: "translateY(10px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        riseIn: "riseIn 0.5s ease-out both",
      },
    },
  },
  plugins: [],
};
