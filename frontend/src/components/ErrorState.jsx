export default function ErrorState({ message, onRetry }) {
  return (
    <div className="max-w-2xl mx-auto px-6 py-16 text-center">
      <p className="text-ink/70 mb-4">
        {message ?? "Не вдалося завантажити дані. Перевірте з'єднання і спробуйте ще раз."}
      </p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-5 py-2 rounded-full bg-espresso text-paper text-sm font-medium hover:bg-ink transition-colors"
        >
          Спробувати ще раз
        </button>
      )}
    </div>
  );
}
