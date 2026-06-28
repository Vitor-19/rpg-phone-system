import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from phone import setup_phone

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    await bot.wait_until_ready()

    synced = await bot.tree.sync()
    print(f"Bot iniciado com sucesso, com {len(synced)} comandos.")


setup_phone(bot)

bot.run(TOKEN)