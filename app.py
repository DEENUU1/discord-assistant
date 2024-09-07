from fastapi import FastAPI
from bot import client, TOKEN
import asyncio
from fastapi_utilities import repeat_every

from useme import task_monitor_useme

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(client.start(TOKEN))


@app.on_event("startup")
@repeat_every(seconds=3600)
async def run_task_monitor_useme():
    await task_monitor_useme()


@app.get("/")
async def read_root():
    await task_monitor_useme()
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
