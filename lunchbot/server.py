from aiohttp import web
from . import run_message
from .config import IMAGE_FOLDER
import logging

logging.basicConfig(level=logging.INFO)

routes = web.RouteTableDef()

@routes.get("/run/amazingsecret")
@routes.post("/run/amazingsecret")
async def request_run(request: web.Request) -> web.Response:
    try:
        logging.info("/run requested")
        await run_message()
        return web.Response(body="ok")
    except BaseException as e:
        logging.error("error wtf", exc_info=e)
        return web.Response(body="whoops", status=500)


async def make_app() -> web.Application:
    app = web.Application()

    app.router.add_static("/preview", IMAGE_FOLDER)
    app.router.add_routes(routes)

    return app


web.run_app(make_app(), port=8888)
