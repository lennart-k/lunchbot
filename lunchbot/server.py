from aiohttp import web
from . import run_message
from .config import IMAGE_FOLDER, RUN_SECRET
import logging

logging.basicConfig(level=logging.INFO)

routes = web.RouteTableDef()

@routes.get(f"/run/{RUN_SECRET}")
@routes.post(f"/run/{RUN_SECRET}")
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

print("Lunchbot Server running on port 8888")
web.run_app(make_app(), port=8888)
