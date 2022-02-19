import discord,os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
botus = commands.Bot(command_prefix='!',intents=discord.Intents.all())
@botus.command()
async def send(ctx,member: discord.Member, *, text):
    print(member)
    print(text)
    await member.send(text)
@botus.event
async def on_ready():
    print(f"Logged in as {botus.user.name}.")
botus.run(os.getenv('token'))