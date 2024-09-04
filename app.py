import os

from fastapi import FastAPI, Query
from pydantic import BaseModel
from bot import client, send_message_to_channel, TOKEN
import asyncio
from enum import Enum

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(client.start(TOKEN))


class ChannelEnum(str, Enum):
    GENERAL = str(os.getenv("CHANNEL_GENERAL", 0))
    USEME = str(os.getenv("CHANNEL_USEME", 0))


class MessageInputSchema(BaseModel):
    content: str


@app.post("/message")
async def send_message(message: MessageInputSchema, channel_id: ChannelEnum = Query(...)):
    await send_message_to_channel(message.content, int(channel_id))
    return {"status": "success"}
