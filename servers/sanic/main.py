from sanic import Sanic, response

app = Sanic("sanic")


@app.route("/echo", methods=["POST"])
async def echo(request):
    data = request.json
    return response.json(data, status=200)
