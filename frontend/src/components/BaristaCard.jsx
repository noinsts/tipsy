import { Blob, CupFace, Heart, Sparks, Underline } from "./Doodles.jsx";

export default function BaristaCard({ barista }) {
  const { name, photoUrl } = barista;

  return (
    <div className="relative px-6 py-5 min-w-[15rem]">
      <Blob className="bg-tint rounded-[2.5rem]" />
      <Sparks className="absolute -left-3 top-0 w-7 h-7 -rotate-12" />

      <div className="relative flex items-center gap-4">
        {photoUrl ? (
          <img
            src={photoUrl}
            alt={name}
            className="w-16 h-16 rounded-full object-cover shrink-0 ring-2 ring-pen/80"
          />
        ) : (
          <CupFace className="shrink-0" />
        )}

        <div className="min-w-0">
          <div className="flex items-start gap-1.5">
            <h3 className="font-hand text-3xl font-semibold leading-none text-pen">{name}</h3>
            <Heart className="w-4 h-4 mt-0.5 shrink-0" />
          </div>
          <Underline className="mt-1 text-pen/80" />
          <p className="text-sm text-pen/60 mt-1.5">Бариста</p>
        </div>
      </div>
    </div>
  );
}
