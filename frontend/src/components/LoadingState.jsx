export default function LoadingState({ label = "Завантаження..." }) {
  return (
    <div className="max-w-2xl mx-auto px-6 py-24 text-center text-pen/60">
      <div className="inline-block h-6 w-6 rounded-full border-2 border-sketch/30 border-t-accent animate-spin mb-3" />
      <p className="font-hand text-2xl">{label}</p>
    </div>
  );
}
