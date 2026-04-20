import discord
import asyncio
from discord.ext import commands, tasks
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

SES_KANAL_ID = 1459873716698877972

# ================= SES BAĞLANTI =================
async def connect_voice():
    await bot.wait_until_ready()

    channel = bot.get_channel(SES_KANAL_ID)
    if not channel:
        print("❌ Kanal bulunamadı!")
        return

    try:
        vc = discord.utils.get(bot.voice_clients, guild=channel.guild)

        if vc is None:
            await channel.connect(reconnect=True)
            print(f"🔊 Bağlandı: {channel.name}")
        elif vc.channel.id != SES_KANAL_ID:
            await vc.move_to(channel)
            print("🔁 Kanal değiştirildi")

    except Exception as e:
        print("❌ Ses hatası:", e)

# ================= LOOP =================
@tasks.loop(minutes=3)  # 🔥 Spam yok
async def voice_loop():
    await connect_voice()

# ================= EVENTS =================
@bot.event
async def on_ready():
    print(f"✅ {bot.user} ses botu aktif!")

    if not voice_loop.is_running():
        voice_loop.start()

# Eğer atılırsa geri gir
@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id and after.channel is None:
        await asyncio.sleep(5)
        await connect_voice()

# ================= BAŞLAT =================
TOKEN = os.getenv("TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("TOKEN YOK!")
