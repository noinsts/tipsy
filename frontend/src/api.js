const API_URL = import.meta.env.VITE_API_URL ?? "-1";

class ApiError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

async function request(path) {
  let response;
  try {
    response = await fetch(`${API_URL}${path}`);
  } catch {
    throw new ApiError(0, "NETWORK_ERROR", "Не вдалося з'єднатися з сервером");
  }

  if (!response.ok) {
    let code = "UNKNOWN_ERROR";
    let message = "Щось пішло не так";
    try {
      const body = await response.json();
      code = body.code ?? code;
      message = body.message ?? message;
    } catch {
      // тіло не JSON — лишаємо дефолтні значення
    }
    throw new ApiError(response.status, code, message);
  }

  return response.json();
}

/** Список усіх закладів: [{ id, name, slug }] */
export function getCafes() {
  return request("/api/v1/public/cafes");
}

/** Хто сьогодні на зміні в закладі: { name, photoUrl, jarUrl }. Кидає 404/SHIFT_NOT_FOUND, якщо нікого. */
export function getShiftBySlug(slug) {
  return request(`/api/v1/public/cafe/${slug}`);
}

export { ApiError };
