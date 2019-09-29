"""

"""

from aiohttp import web
from aiohttp.web import Request

from lidarproc.main.data_retrieval import LidarThread


__author__ = ["Clément Besnier <clemsciences@aol.com>", ]


async def on_startup(app):
    app["lidar"] = LidarThread()


async def on_shutdown(app):
    app["lidar"].close_connection()

routes = web.RouteTableDef()
@routes.post("/get_measures")
async def get_measures(request: Request):
    print(request)
    lidar_turn_data = request.app["lidar"].get_measures()
    data = {"measures": lidar_turn_data,
            "success": True}
    return web.json_response(data)


@routes.post("/manage_lidar")
async def manage_lidar(request: Request):
    response = request.json()
    if "action" in response:
        action = response["action"]
        if action == "start":
            pass
        elif action == "stop":
            pass

    data = {'success': True}
    return web.json_response(data)

if __name__ == "__main__":
    lidar_app = web.Application()
    lidar_app.on_startup.append(on_startup)
    lidar_app.on_shutdown.append(on_shutdown)
    lidar_app.add_routes(routes)
    web.run_app(lidar_app, port=8090)
