from fastapi import FastAPI

app = FastAPI()


@app.post("/echo")
async def echo(data: dict):
    return data
