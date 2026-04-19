import os
import discord
import asyncio
from discord.ext import commands

# ================= AYARLAR =================
SES_KANAL_ID = 1495031512729518242 

intents = discord.Intents.default()
intents.voice_states = True 
bot = commands.Bot(command_prefix="afk!", intents=intents)

# ================= FONKSİYONLAR =================

async def join_voice_channel():
    """Botun kanalı bulmasını ve AFK olarak girmesini sağlar."""
    try:
        # get_channel yerine fetch_channel kullanarak kanalı zorla buluyoruz
        channel = await bot.fetch_channel(SES_KANAL_ID)
        
        if not channel or not isinstance(channel, discord.VoiceChannel):
            print(f"❌ HATA: {SES_KANAL_ID} ID'li bir SES kanalı bulunamadı!")
            return

        # Mevcut ses bağlantısını kontrol et
        vc = discord.utils.get(bot.voice_clients, guild=channel.guild)

        if not vc:
            await channel.connect(reconnect=True, timeout=20, self_deaf=True, self_mute=True)
            print(f"🔊 {channel.name} kanalına başarıyla giriş yapıldı.")
        elif vc.channel.id != SES_KANAL_ID:
            await vc.move_to(channel)
            
    except discord.NotFound:
        print("❌ HATA: Kanal bulunamadı. ID yanlış olabilir veya bot bu sunucuda değil.")
    except discord.Forbidden:
        print("❌ HATA: Botun bu kanalı görme/bağlanma yetkisi yok!")
    except Exception as e:
        print(f"❌ Beklenmedik bir hata oluştu: {e}")

# ================= OLAYLAR =================

@bot.event
async def on_ready():
    print(f"✅ {bot.user} AFK Botu Aktif!")
    
    # Botun kendine gelmesi için 3 saniye bekle
    await asyncio.sleep(3)
    await join_voice_channel()
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Worsy AFK 7/24"))

@bot.event
async def on_voice_state_update(member, before, after):
    # Bot sesten düşerse geri girer
    if member.id == bot.user.id and after.channel is None:
        print("⚠️ Sesten düşüldü, geri bağlanılıyor...")
        await asyncio.sleep(5)
        await join_voice_channel()

# ================= ÇALIŞTIR =================
TOKEN = os.getenv("TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("HATA: TOKEN bulunamadı!")
