import os
import fastapi, uvicorn

app = fastapi.FastAPI()


@app.get("current-stat/")
async def current_stat():
    return {"hello": "world"}


uvicorn.run(app=app, host="0.0.0.0")
