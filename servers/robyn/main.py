from robyn import Robyn

app = Robyn(__file__)


@app.post("/echo")
async def h(request):
    return request.body


app.start("0.0.0.0", port=8000)
