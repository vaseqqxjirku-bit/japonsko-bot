import discord
from discord.ext import commands
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- FIX PRO RENDER (Drží port otevřený 24/7, aby to netimeoutovalo) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Radio Bot is online 24/7!")
    def log_message(self, format, *args):
        pass

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()
# -------------------------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Vysílačka je online 24/7 jako {bot.user}")

@bot.command()
async def pripojit(ctx):
    """Připojí bot do tvého hlasového kanálu"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🎙️ Vysílačka se připojila do kanálu: **{channel.name}**")
    else:
        await ctx.send("❌ Musíš být v nějakém hlasovém kanálu!", ephemeral=True)

@bot.command()
async def odpojit(ctx):
    """Odpojí bot z hlasového kanálu"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Vysílačka se odpojila.")
    else:
        await ctx.send("❌ Bot není v žádném hlasovém kanálu.", ephemeral=True)

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
