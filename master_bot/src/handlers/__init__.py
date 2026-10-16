from aiogram import Router

from .cafes import CafeHandler
from .common import CommonHandler
from .employees import EmployeeHandler
from ..middlewares.access import AccessMiddleware


def get_main_router() -> Router:
    router = Router()
    handlers = (CommonHandler(), EmployeeHandler(), CafeHandler())

    # Attach the allow-list check to each child observer so it also protects
    # handlers registered inside subrouters (not only handlers on this router).
    for handler in handlers:
        child_router = handler.get_router()
        access_middleware = AccessMiddleware()
        child_router.message.outer_middleware(access_middleware)
        child_router.callback_query.outer_middleware(access_middleware)
        router.include_router(child_router)

    return router
