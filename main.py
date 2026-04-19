import os
import discord
import asyncio
from discord.ext import commands

# ================= AYARLAR =================
# Buraya botun duracağı ses kanalının ID'sini yaz
SES_KANAL_ID = 1495031512729518242 

intents = discord.Intents.default()
intents.voice_states = True # Ses durumlarını izlemek için şart
bot = commands.Bot(command_prefix="afk!", intents=intents)

# ================= FONKSİYONLAR =================

async def join_voice_channel():
    """Botun belirlenen kanala AFK (sessiz/sağır) girmesini sağlar."""
    channel = bot.get_channel(SES_KANAL_ID)
    if not channel:
        print(f"❌ HATA: {SES_KANAL_ID} ID'li kanal bulunamadı. ID'yi kontrol et!")
        return

    # Mevcut ses bağlantılarını kontrol et
    vc = discord.utils.get(bot.voice_clients, guild=channel.guild)

    try:
        if not vc:
            # self_deaf=True: Kulaklık Kapalı | self_mute=True: Mikrofon Kapalı
            await channel.connect(reconnect=True, timeout=20, self_deaf=True, self_mute=True)
            print(f"🔊 {channel.name} kanalına AFK olarak giriş yapıldı.")
        elif vc.channel.id != SES_KANAL_ID:
            await vc.move_to(channel)
    except Exception as e:
        print(f"❌ Ses bağlantı hatası: {e}")

# ================= OLAYLAR =================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} AFK Botu Hazır!")
    # Bot açılır açılmaz kanala girer
    await join_voice_channel()
    
    # Botun durumunu (Activity) ayarla
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="7/24 Worsy Voice"))

@bot.event
async def on_voice_state_update(member, before, after):
    """Bot kanaldan atılırsa veya sesten düşerse otomatik geri döner."""
    if member.id == bot.user.id and after.channel is None:
        print("⚠️ Sesten düşüldü, 5 saniye içinde geri bağlanılıyor...")
        await asyncio.sleep(5)
        await join_voice_channel()

# ================= ÇALIŞTIR =================
# Railway panelinden 'TOKEN' isminde bir değişken oluşturup botun tokenini yapıştır
TOKEN = os.getenv("TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("HATA: TOKEN değişkeni bulunamadı! Railway ayarlarını kontrol et.")
