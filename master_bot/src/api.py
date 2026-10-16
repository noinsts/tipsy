import json
import os
from typing import Any
import aiohttp

BACKEND_URL = os.getenv("BACKEND_URL", "localhost:8080").strip().rstrip("/")
BOT_INTERNAL_TOKEN = os.getenv("BOT_INTERNAL_TOKEN", "")


def _base_url() -> str:
    """Return a valid backend URL, accepting both host:port and full URLs."""
    value = BACKEND_URL
    if not value:
        raise RuntimeError("Не задано BACKEND_URL")
    if not value.startswith(("http://", "https://")):
        value = f"http://{value}"
    return value.rstrip("/")


class ApiError(RuntimeError):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
        super().__init__(message)


async def _request(
    method: str,
    path: str,
    *,
    json_data: dict[str, Any] | None = None,
    data: aiohttp.FormData | None = None,
    params: dict[str, Any] | None = None,
    authenticated: bool = True,
) -> Any:
    headers = {}
    if authenticated:
        if not BOT_INTERNAL_TOKEN:
            raise RuntimeError("Не задано BOT_INTERNAL_TOKEN")
        headers["X-Bot-Token"] = BOT_INTERNAL_TOKEN

    timeout = aiohttp.ClientTimeout(total=20)
    url = f"{_base_url()}{path}"
    try:
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            async with session.request(
                method,
                url,
                json=json_data,
                data=data,
                params=params,
            ) as response:
                body_text = await response.text()
                if not 200 <= response.status < 300:
                    message = f"Помилка API ({response.status})"
                    if body_text:
                        try:
                            body = json.loads(body_text)
                            message = body.get("detail") or body.get("message") or body.get("error") or message
                        except (json.JSONDecodeError, AttributeError):
                            message = body_text[:500] or message
                    raise ApiError(response.status, str(message))

                if response.status == 204 or not body_text.strip():
                    return None
                try:
                    return json.loads(body_text)
                except json.JSONDecodeError as exc:
                    raise RuntimeError("Бекенд повернув некоректну JSON-відповідь") from exc
    except (aiohttp.ClientError, TimeoutError) as exc:
        raise RuntimeError("Не вдалося з’єднатися з бекендом") from exc


# Public data
async def fetch_all_cafes() -> list[dict[str, Any]]:
    result = await _request("GET", "/api/v1/public/cafes", authenticated=False)
    return result if isinstance(result, list) else []


# Employee CRUD
async def fetch_all_employees() -> list[dict[str, Any]]:
    result = await _request("GET", "/api/v1/bot/employees")
    return result if isinstance(result, list) else []


async def fetch_employee(employee_id: int) -> dict[str, Any]:
    return await _request("GET", f"/api/v1/bot/employees/{employee_id}")


async def create_employee(payload: dict[str, Any]) -> dict[str, Any]:
    return await _request("POST", "/api/v1/bot/employees", json_data=payload)


async def update_employee(employee_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    return await _request("PUT", f"/api/v1/bot/employees/{employee_id}", json_data=payload)


async def delete_employee(employee_id: int) -> None:
    await _request("DELETE", f"/api/v1/bot/employees/{employee_id}")


# Cafe CRUD
async def fetch_cafe(cafe_id: int) -> dict[str, Any]:
    return await _request("GET", f"/api/v1/bot/cafes/{cafe_id}")


async def fetch_all_managed_cafes() -> list[dict[str, Any]]:
    result = await _request("GET", "/api/v1/bot/cafes")
    return result if isinstance(result, list) else []


async def create_cafe(payload: dict[str, Any]) -> dict[str, Any]:
    return await _request("POST", "/api/v1/bot/cafes", json_data=payload)


async def update_cafe(cafe_id: int, payload: dict[str, Any]) -> dict[str, Any]:
    return await _request("PUT", f"/api/v1/bot/cafes/{cafe_id}", json_data=payload)


async def delete_cafe(cafe_id: int) -> None:
    await _request("DELETE", f"/api/v1/bot/cafes/{cafe_id}")


async def upload_photo_api(data: bytes, filename: str, content_type: str) -> str:
    form = aiohttp.FormData()
    form.add_field("file", data, filename=filename, content_type=content_type)
    body = await _request("POST", "/api/v1/bot/images", data=form)
    photo_url = body.get("url") if isinstance(body, dict) else None
    if not photo_url:
        raise RuntimeError("Бекенд не повернув посилання на фото")
    return photo_url
