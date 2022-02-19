import discord
import functions
import datetime
import os
import warnings
import aiohttp
import time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
warnings.filterwarnings("ignore", category=DeprecationWarning)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), self_bot=True)
bot.session = aiohttp.ClientSession()
client = discord.Client()
sent_users = []


@bot.event
async def timeout_user(*, user_id: int, guild_id: int, until):
    headers = {"Authorization": f"Bot {bot.http.token}"}
    url = f"https://discord.com/api/v9/guilds/{guild_id}/members/{user_id}"
    timeout = (datetime.datetime.utcnow() + datetime.timedelta(minutes=until)).isoformat()
    json = {'communication_disabled_until': timeout}
    async with bot.session.patch(url, json=json, headers=headers) as session:
        if session.status in range(200, 299):
            return True
        return False


@bot.listen("on_message")
async def scam(message):
    distance = {}
    URLs = functions.findURLs(message.content)
    joinDate = message.author.joined_at
    currentTime = datetime.datetime.now()
    timeDifference = currentTime - joinDate
    scam = {"reason": [], "percentage": 0}

    for url in URLs:
        # Iterating over all URLs found in the message.

        dist = functions.levenshteinDistanceDP(url, "https://discord.com")
        distance[url] = dist
        # Getting the distance between an actual Discord URL and a fake one.

        if url in functions.scamLinks:
            # If URL is in known scam URLs, set scam to True.
            scam['reason'].append(f"URL ({url}) is a verified scam link.")
            scam['percentage'] = 100

    for word in functions.scamWordsList:
        # Iterating over all words scammers commonly use.
        if word in message.content:
            scam['percentage'] += 10
            scam['reason'].append(f"Word ({word}) is suspicious word.")

    for url, distance in distance.items():
        # Going through all URLs found in the message and checking if they are close to a Discord URL.
        if distance <= 7:
            if distance != 0:
                scam['percentage'] += 20
                scam['reason'].append(f"URL ({url}) is suspicious.")
    if timeDifference is not None:
        if int(timeDifference.days) <= 1:
            # Checks to see if user has been a part of the server for less than a day before sending this message.
            scam['percentage'] += 30
            scam['reason'].append(f"Age in server (<t:{int(time.mktime(joinDate.timetuple()))}:R>) is suspicious.")
    channel = await bot.fetch_channel(536719908080189450)
    moderator = discord.utils.get(message.guild.roles, id=461636038406832134)
    x = '\n'.join(scam['reason'])
    if scam['percentage'] >= 50:
        await message.delete()
        await channel.send(
            embed=discord.Embed(title=f"{scam['percentage']}% likely to be a scam.", description=f"Reason(s): {x}",
                                color=0x126180))
        await message.author.send(
            embed=discord.Embed(
                title=f"Your message in the Si Not Found discord server was read as a scam and you were timed out for 1 week. Please respond to this message to appeal your timeout with the mods by doing @JawsBot followed by your message",
                color=0x126180))

        handshake = await timeout_user(user_id=message.author.id, guild_id=message.author.guild.id, until=10080)
        if handshake:
            return await channel.send(f"{moderator.mention} Successfully timed out {message.author} for 1 week")
        await channel.send(f"{moderator.mention}Something went wrong and {message.author} was not timed out")

    await bot.process_commands(message)


@bot.listen("on_message")
async def messages(message):
    if message.guild:
        return
    if message.author == bot.user:
        return
    modmail_channel = await bot.fetch_channel(536719908080189450)
    await message.author.send(embed=discord.Embed(title=f'Your message has been sent to the mods.The mod team will get back to you as soon as they can. Please **DO NOT** spam this bot or else your timeout will not be appealed and you will be banned', color=0x00FFFF))
    sent_users.append(message.author.id)
    if message.author.send:
        await modmail_channel.send(embed=discord.Embed(title=f"from {message.author}", description=f"Their message is '{message.content}' .To respond please do !send @*the user* *your message", color=0x126180))

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}.")


print(functions.scamLinks)
bot.run(os.getenv('token'))
