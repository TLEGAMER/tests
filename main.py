import discord
from discord.ext import commands, tasks
from wavelink import Node, NodePool, Player, YouTubeTrack
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix='!', intents=intents)

GUILD_ID = 1369585458434019349     # ใส่ guild ID
VC_CHANNEL_ID = 1375227595741855825   # ใส่ voice channel ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await connect_lavalink()
    await auto_rejoin()

async def connect_lavalink():
    await NodePool.create_node(bot=bot,
                                host='127.0.0.1',
                                port=2333,
                                password='youshallnotpass',
                                region='us_central')

async def auto_rejoin():
    await bot.wait_until_ready()
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(VC_CHANNEL_ID)
    if channel:
        await channel.connect(cls=Player)

@bot.command()
async def summon(ctx):
    if ctx.author.voice:
        vc = ctx.author.voice.channel
        await vc.connect(cls=Player)
        await ctx.send(f'เข้าร่วม {vc.name} แล้ว!')
    else:
        await ctx.send('คุณต้องอยู่ในห้องเสียงก่อน')

@bot.command()
async def play(ctx, *, search: str):
    if not ctx.voice_client:
        await ctx.send("บอทยังไม่อยู่ในห้องเสียง ใช้ !summon ก่อน")
        return

    tracks = await YouTubeTrack.search(search)
    track = tracks[0]
    await ctx.voice_client.play(track)
    await ctx.send(f'กำลังเล่น: {track.title}')

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("หยุดเล่นและออกจากห้องเสียงแล้ว")

# สำหรับ render.com ป้องกันบอทหยุด
from keep_alive import keep_alive
keep_alive()

bot.run(os.getenv("DISCORD_TOKEN"))
