from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


# Define a function to handle POST requests
async def echo(request):
    data = await request.json()
    return JSONResponse(data)


app = Starlette(
    routes=[
        Route("/echo", endpoint=echo, methods=["POST"]),
    ]
)
