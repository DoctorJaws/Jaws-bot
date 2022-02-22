import discord,os
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
botus = commands.Bot(command_prefix='!',intents=discord.Intents.all())
@botus.command()
async def send(ctx,member: discord.Member, *, text):
    print(member)
    print(text)
    await member.send(embed=discord.Embed(title=f"the mods have seen your message and say: a scam.", description=f"{text}",
                                color=0x126180))
@botus.command()
async def code(ctx):
    await ctx.send("https://github.com/DoctorJaws/Jaws-bot")
@botus.event
async def on_ready():
    print(f"Logged in as {botus.user.name}.")
botus.run(os.getenv('token'))
