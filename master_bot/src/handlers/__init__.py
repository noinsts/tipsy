from aiogram import Router

from .common import CommonHandler

from ..middlewares.access import AccessMiddleware

def get_main_router() -> Router:
    router = Router()

    access_middleware = AccessMiddleware()

    router.message.middleware(access_middleware)
    router.callback_query.middleware(access_middleware)

    routers = [
        CommonHandler().get_router(),
    ]

    for r in routers:
        router.include_router(r)

    return router