export default function LoadingState({ label = "Завантаження..." }) {
  return (
    <div className="max-w-2xl mx-auto px-6 py-16 text-center text-ink/50">
      <div className="inline-block h-5 w-5 rounded-full border-2 border-ink/20 border-t-sage animate-spin mb-3" />
      <p>{label}</p>
    </div>
  );
}
