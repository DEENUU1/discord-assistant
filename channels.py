import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()


class ChannelEnum(str, Enum):
    GENERAL = str(os.getenv("CHANNEL_GENERAL", 0))
    USEME = str(os.getenv("CHANNEL_USEME", 0))
