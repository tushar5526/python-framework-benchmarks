from litestar import Litestar, post


@post("/")
async def echo(data: dict[str, str]) -> dict[str, str]:
    """Keeping the tradition alive with hello world."""
    return data


app = Litestar(route_handlers=[echo])
