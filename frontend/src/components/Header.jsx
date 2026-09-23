import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header className="border-b border-espresso/10">
      <div className="max-w-2xl mx-auto px-6 py-6">
        <Link
          to="/"
          className="font-display text-xl text-espresso tracking-tight hover:text-sageDark transition-colors"
        >
            Zone Coffee | Green Donner
        </Link>
      </div>
    </header>
  );
}
