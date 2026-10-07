export default function ErrorState({ message, onRetry }) {
  return (
    <div className="max-w-2xl mx-auto px-6 py-24 text-center">
      <p className="text-pen/70 mb-5">
        {message ?? "Не вдалося завантажити дані. Перевірте з'єднання і спробуйте ще раз."}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-6 py-2.5 rounded-full bg-accent text-white text-sm font-medium hover:bg-accentDark transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-accentDark"
        >
          Спробувати ще раз
        </button>
      )}
    </div>
  );
}
