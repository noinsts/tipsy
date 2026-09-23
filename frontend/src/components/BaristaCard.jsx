function initials(name) {
    if (!name) return "";
    return name
        .split(" ")
        .filter(Boolean)
        .slice(0, 2)
        .map((part) => part[0])
        .join("")
        .toUpperCase();
}

export default function BaristaCard({ barista }) {
    const { name, photoUrl, jarUrl } = barista;

    return (
        <div className="animate-riseIn max-w-sm w-full mx-auto">
            <div className="tear-edge h-3 bg-espresso rounded-t-2xl" />
            <div className="bg-espresso rounded-b-2xl px-8 py-10 text-center shadow-[0_20px_40px_-24px_rgba(35,25,18,0.5)]">
                {photoUrl ? (
                    <img
                        src={photoUrl}
                        alt={name}
                        className="w-24 h-24 rounded-full object-cover mx-auto mb-5 ring-2 ring-gold/60"
                    />
                ) : (
                    <div className="w-24 h-24 rounded-full mx-auto mb-5 ring-2 ring-gold/60 bg-sage flex items-center justify-center">
                        <span className="font-display text-2xl text-paper">{initials(name)}</span>
                    </div>
                )}

                <p className="text-paper/60 text-sm mb-1">Сьогодні на зміні</p>
                <h2 className="font-display text-2xl text-paper mb-6">{name}</h2>

                {jarUrl ? (
                    <a
                        href={jarUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-block px-6 py-2.5 rounded-full bg-gold text-espresso text-sm font-medium hover:bg-gold/90 transition-colors"
                    >
                        Залишити чайові
                    </a>
                ) : (
                    <p className="text-paper/40 text-sm">Банку для чайових ще не додано</p>
                )}
            </div>
        </div>
    );
}