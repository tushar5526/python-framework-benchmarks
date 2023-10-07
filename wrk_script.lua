wrk.method = "POST"
wrk.body = '{"name": "Hello Benchmark!"}'  -- Replace with the name you want to send in the request
wrk.headers["Content-Type"] = "application/json"

