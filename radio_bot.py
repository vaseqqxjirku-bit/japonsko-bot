import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID_TO_PING = 1564306169105748040  # <--- TADY PŘEPIŠ TOHLE ČÍSLO ZA ID TVÉ ROLE RODINA

FREQ_MIN = 100.00
FREQ_MAX = 999.99

def generate_freq():
    return f"{random.uniform(FREQ_MIN, FREQ_MAX):.2f}"

def create_radio_embed(current_freq: str, prev_freq: str = "---", user: discord.Member = None):
    embed = discord.Embed(
        title="🇯🇵 VYSÍLAČKA 🇯🇵",
        color=discord.Color.from_rgb(188, 0, 45)
    )
    embed.add_field(name="Předchozí frekvence", value=f"`{prev_freq} MHz`", inline=False)
    embed.add_field(name="Aktuální frekvence", value=f"# `📡 {current_freq} MHz`", inline=False)
    
    if user:
        embed.set_footer(text=f"Naposledy změnil: {user.display_name}", icon_url=user.display_avatar.url)
    else:
        embed.set_footer(text="Japonský vysílačkový systém")
    return embed

class RadioView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Změna freq (případ nouze)", style=discord.ButtonStyle.danger, emoji="🆘", custom_id="change_freq_emergency")
    async def change_freq_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        old_embed = interaction.message.embeds[0]
        
        old_current = "---"
        if len(old_embed.fields) > 1:
            val = old_embed.fields[1].value
            old_current = val.replace("#", "").replace("`", "").replace("📡", "").strip().replace(" MHz", "")
        
        new_freq = generate_freq()
        
        embed = discord.Embed(
            title="🇯🇵 VYSÍLAČKA 🇯🇵",
            color=discord.Color.from_rgb(188, 0, 45)
        )
        embed.add_field(name="Předchozí frekvence", value=f"`{old_current} MHz`", inline=False)
        embed.add_field(name="Aktuální frekvence", value=f"# `📡 {new_freq} MHz`", inline=False)
        embed.set_footer(text=f"Změnil: {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
        
        await interaction.response.edit_message(embed=embed, view=self)
        
        mention = f"<@&{ROLE_ID_TO_PING}>"
        await interaction.channel.send(
            content=f"🚨 {mention} **ZMĚNA FREKVENCE!**\nNová freq: **`{new_freq} MHz`** *(Změnil: {interaction.user.mention})*",
            allowed_mentions=discord.AllowedMentions(roles=True)
        )

@bot.event
async def on_ready():
    bot.add_view(RadioView())
    print(f"Bot je online jako {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def vysilacka(ctx):
    await ctx.message.delete()
    initial_freq = generate_freq()
    embed = create_radio_embed(initial_freq)
    await ctx.send(embed=embed, view=RadioView())

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
