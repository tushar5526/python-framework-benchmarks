from quart import Quart, request, jsonify

app = Quart(__name__)


@app.route("/echo", methods=["POST"])
async def echo():
    data = await request.get_json()
    return jsonify(data)
