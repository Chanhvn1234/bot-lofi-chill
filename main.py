import discord
import asyncio
import yt_dlp
import os
from discord.ext import commands
from dotenv import load_dotenv

# Nhúng web mini chống ngủ
from keep_alive import keep_alive 

load_dotenv()

# ==================== CẤU HÌNH THÔNG TIN ====================
BOT_TOKEN = os.getenv("DISCORD_TOKEN") 
VOICE_CHANNEL_ID = 1522932283395276870  # <<< ÔNG NHỚ ĐIỀN ID PHÒNG VÀO NHA

LOFI_10H_URL = "https://youtu.be/JCKBaJDRMw4?si=7dH1HhzA-r0JWR7w"  
# ============================================================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ffmpeg_options = {
    'options': '-vn',
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True
}

async def play_infinite_loop(vc):
    while True:
        if not vc.is_playing() and not vc.is_paused():
            try:
                print("[Hệ thống] Đang kéo luồng âm thanh mới...")
                loop = asyncio.get_event_loop()
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = await loop.run_in_executor(None, lambda: ydl.extract_info(LOFI_10H_URL, download=False))
                    audio_url = info['url']
                    title = info.get('title', 'Video Lofi 10 Tiếng')

                print(f"▶️ [BẮT ĐẦU VÒNG LẶP] {title}")
                
                # Đã sửa cấu hình để chạy được trên Linux (Replit)
                vc.play(discord.FFmpegPCMAudio(audio_url, executable="ffmpeg", **ffmpeg_options))
                
                while vc.is_playing() or vc.is_paused():
                    await asyncio.sleep(5)
                    
            except Exception as e:
                print(f"[Cảnh báo] Mạng chập chờn, thử lại sau 5s... Lỗi: {e}")
                await asyncio.sleep(5)
        else:
            await asyncio.sleep(5)

@bot.event
async def on_ready():
    print(f"=== {bot.user.name} Đã Hạ Cánh Lên Đám Mây ===")
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        vc = discord.utils.get(bot.voice_clients, guild=channel.guild)
        if not vc:
            try:
                vc = await channel.connect()
            except Exception as e:
                return
        bot.loop.create_task(play_infinite_loop(vc))

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id and after.channel is None:
        await asyncio.sleep(5)
        channel = bot.get_channel(VOICE_CHANNEL_ID)
        if channel:
            try:
                vc = await channel.connect()
                bot.loop.create_task(play_infinite_loop(vc))
            except Exception:
                pass

# Kích hoạt web chống ngủ trước khi chạy bot
keep_alive() 

bot.run(BOT_TOKEN)
