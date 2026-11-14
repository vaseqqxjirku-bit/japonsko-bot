import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Vysilacka Bot is online 24/7!")
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Vysílačka Bot je online jako {bot.user}")

@bot.command()
async def vysilacka(ctx, *, zprava: str = "Žádná zpráva"):
    try:
        await ctx.message.delete()
    except:
        pass
    embed = discord.Embed(
        title="📻 VYSÍLAČKA / DISPATCH",
        description=zprava,
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Autor: {ctx.author.display_name}")
    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
