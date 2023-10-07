.PHONY: fastapi benchmark quart flask robyn sanic litestar

fastapi:
	uvicorn servers.fastapi.main:app --host 0.0.0.0 --port 8000 --workers 16

flask:
	gunicorn -w 15 --threads 16 -b 0.0.0.0:8000 servers.flask.main:app

quart:
	uvicorn servers.quart.main:app --host 0.0.0.0 --port 8000 --workers 16

robyn:
	python servers/robyn/main.py --processes 16 --workers 16

sanic:
	uvicorn servers.sanic.main:app --host 0.0.0.0 --port 8000 --workers 16

starlette:
	uvicorn servers.starlette.main:app --host 0.0.0.0 --port 8000 --workers 16

starlite:
	uvicorn servers.starlite.main:app --host 0.0.0.0 --port 8000 --workers 16

litestar:
	uvicorn servers.litestar.main:app --host 0.0.0.0 --port 8000 --workers 16

benchmark:
	wrk -t12 -c400 -d10s -s wrk_script.lua http://localhost:8000/echo