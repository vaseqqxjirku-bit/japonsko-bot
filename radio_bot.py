import discord
from discord.ext import commands
import random
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_ID_TO_PING = 123456789012345678  # <--- TADY SI PŘEPIŠ ID SVÉ ROLE RODINA

FREQ_MIN = 100.00
FREQ_MAX = 999.99

def generate_freq():
    return f"{random.uniform(FREQ_MIN, FREQ_MAX):.2f}"

def create_radio_embed(current_freq: str, prev_freq: str = "---", user: str = "Nikdo", reason: str = "Zatím bez změn"):
    embed = discord.Embed(
        title="🇯🇵 VYSÍLAČKA 🇯🇵",
        color=discord.Color.from_rgb(188, 0, 45)
    )
    embed.add_field(name="Předchozí frekvence", value=f"`{prev_freq} MHz`", inline=False)
    embed.add_field(name="Aktuální frekvence", value=f"# `📡 {current_freq} MHz`", inline=False)
    embed.add_field(name="Poslední změna", value=f"**Uživatel:** {user}\n**Důvod:** *{reason}*", inline=False)
    embed.set_footer(text="Japonský vysílačkový systém")
    return embed

class ReasonModal(discord.ui.Modal, title="Nouzová změna frekvence"):
    reason_input = discord.ui.TextInput(
        label="Důvod změny frekvence",
        style=discord.TextStyle.short,
        placeholder="Např. Policie v patách, úprk z lokace...",
        required=True,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):
        old_embed = interaction.message.embeds[0]
        
        old_current = "---"
        if len(old_embed.fields) > 1:
            val = old_embed.fields[1].value
            old_current = val.replace("#", "").replace("`", "").replace("📡", "").strip().replace(" MHz", "")
        
        new_freq = generate_freq()
        reason_text = self.reason_input.value
        user_name = interaction.user.display_name
        
        # Aktualizace hlavního panelu vysílačky
        embed = create_radio_embed(new_freq, old_current, user_name, reason_text)
        await interaction.response.edit_message(embed=embed, view=RadioView())
        
        # Odeslání pingu s rolí a nastavením mazání po 5 minutách (300 vteřin)
        mention = f"<@&{ROLE_ID_TO_PING}>"
        alert_msg = await interaction.channel.send(
            content=f"🚨 {mention} **NOUZOVÁ ZMĚNA FREKVENCE!**\nNová freq: **`{new_freq} MHz`**\n**Změnil:** {interaction.user.mention}\n**Důvod:** *{reason_text}*\n*(Tato zpráva se za 5 minut sama smaže)*",
            allowed_mentions=discord.AllowedMentions(roles=True)
        )
        
        # Časovač na smazání po 5 minutách (300 vteřin)
        await asyncio.sleep(300)
        try:
            await alert_msg.delete()
        except discord.HTTPException:
            pass

class RadioView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="SOS", style=discord.ButtonStyle.danger, emoji="🚨", custom_id="change_freq_emergency")
    async def change_freq_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Otevře vyskakovací formulář pro zadání důvodu
        await interaction.response.send_modal(ReasonModal())

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
