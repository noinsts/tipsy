# coffee-frontend

React + Vite + Tailwind. Дві сторінки:

- `/` — список усіх закладів
- `/point/:id` — картка того, хто зараз на зміні в цьому закладі

`:id` у маршруті — це насправді **slug** закладу (напр. `cafe-1`), таким, як його
повертає бекенд у `GET /api/cafes`. Числовий `id` з БД тут не використовується,
бо публічний ендпоінт `current-barista` прив'язаний саме до slug.

## Запуск

```bash
cp .env.example .env      # вкажіть VITE_API_URL, якщо бекенд не на localhost:8080
npm install
npm run dev
```

## Білд

```bash
npm run build             # результат у dist/
npm run preview           # локально подивитись білд
```

## Що використовується з бекенду

Тільки публічні (без токена) ендпоінти:

- `GET /api/cafes` → `[{ id, name, slug }]`
- `GET /api/cafes/{slug}/current-barista` → `{ name, photoUrl, jarUrl }` або 404 `SHIFT_NOT_FOUND`

## Структура

```
src/
├── api.js                 клієнт до бекенду
├── App.jsx                роутинг
├── components/
│   ├── Header.jsx
│   ├── BaristaCard.jsx
│   ├── LoadingState.jsx
│   └── ErrorState.jsx
└── pages/
    ├── Home.jsx            "/"
    └── CafePoint.jsx       "/point/:id"
```
