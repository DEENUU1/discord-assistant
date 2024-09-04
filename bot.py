import os
from dotenv import load_dotenv
import discord

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_connect():
    print("Bot connected")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')


async def send_message_to_channel(message: str, channel_id: int):
    channel = client.get_channel(channel_id)
    if not channel:
        print(f"Channel with ID {channel_id} not found.")
        return
    await channel.send(message)


if __name__ == "__main__":
    client.run(TOKEN)
