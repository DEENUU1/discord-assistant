import requests
import os
from dotenv import load_dotenv
from logging import getLogger
from typing import Optional

from bot import send_message_to_channel
from channels import ChannelEnum

load_dotenv()

logger = getLogger(__name__)


def get_new_offers(category_url: str) -> Optional[list[dict]]:
    try:
        response = requests.post(os.getenv("USEME_API_URL"), data={"url": category_url})

        if response.status_code == 200:
            return response.json()

    except Exception as e:
        logger.error(e)
        return


def split_response_to_chunks(data: list[dict], chunK_size: int = 2000) -> list[str]:
    formatted_entries = [f"- {item['title']} - {item['url']}" for item in data]
    chunks = []
    current_chunk = ""

    for entry in formatted_entries:
        if len(current_chunk) + len(entry) + 2 > chunK_size:
            chunks.append(current_chunk)
            current_chunk = entry
        else:
            if current_chunk:
                current_chunk += "\n" + entry
            else:
                current_chunk = entry

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


async def task_monitor_useme() -> None:
    try:
        categories = [
            "https://useme.com/pl/jobs/category/serwisy-internetowe,34/",
            "https://useme.com/pl/jobs/category/programowanie-i-it,35/"
        ]

        logger.info("Checking for new offers")

        for category in categories:
            logger.info(f"Checking category: {category}")
            offers = get_new_offers(category)
            if offers:
                logger.info(f"Found {len(offers)} new offers")

                chunks = split_response_to_chunks(offers)
                logger.info(f"Sending {len(chunks)} messages")

                for chunk in chunks:
                    logger.info(f"Sending message: {chunk}")
                    await send_message_to_channel(chunk, channel_id=int(ChannelEnum.USEME.value))

            else:
                logger.info("No new offers")
                await send_message_to_channel("No new offers", channel_id=int(ChannelEnum.USEME.value))

    except Exception as e:
        logger.error(e)
        return
