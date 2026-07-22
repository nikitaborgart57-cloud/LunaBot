from flask import Flask
import threading, os, asyncio
import discord
from discord.ext import commands
from discord import ui

app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run_web():
    # use_reloader=False - ЭТО ФИКСИТ ТВОЙ 429 БАН!
    app.run(host='0.0.0.0', port=10000, use_reloader=False)

threading.Thread(target=run_web, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class CloseTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="Закрыть тикет", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_message("Тикет закроется через 5 сек...", ephemeral=True)
        await asyncio.sleep(5)
        try: await interaction.channel.delete()
        except: pass

class TicketSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Пожаловаться на пользователя", emoji="👤"),
            discord.SelectOption(label="Пожаловаться на состав", emoji="👮"),
            discord.SelectOption(label="Подать заявку на должность", emoji="📝"),
            discord.SelectOption(label="Другое...", emoji="❓"),
        ]
        super().__init__(placeholder="Выбери тему", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
        embed = discord.Embed(title=f"Тикет: {self.values[0]}", description=f"{interaction.user.mention} Опиши проблему!", color=0x2B2D31)
        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"Тикет создан: {channel.mention}", ephemeral=True)

class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.event
async def on_ready():
    print(f"Бот онлайн {bot.user}")
    try: await bot.tree.sync()
    except Exception as e: print(e)

@bot.command(name="поддержка")
async def support(ctx):
    embed = discord.Embed(title="Обратиться в поддержку", description="Выберите тему тикета", color=0x2B2D31)
    await ctx.send(embed=embed, view=TicketView())

bot.run(os.getenv("DISCORD_TOKEN"))
