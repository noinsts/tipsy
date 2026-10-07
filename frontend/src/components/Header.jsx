import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header>
      <div className="max-w-4xl mx-auto px-6 pt-6">
        <Link
          to="/"
          className="font-hand text-2xl font-semibold text-pen hover:text-accentDark transition-colors"
        >
          Zona Coffee | Green Doner
        </Link>
      </div>
    </header>
  );
}
