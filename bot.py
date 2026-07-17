from flask import Flask
import threading

app = Flask('')
@app.route('/')
def home():
    return "LunaBot is online!"
def run_web():
    app.run(host='0.0.0.0', port=10000)
threading.Thread(target=run_web).start()

import discord, os, asyncio
from discord import ui
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

class CloseTicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @ui.button(label="🔒 Закрыть тикет", style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: ui.Button):
        is_admin = interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_channels
        has_role = any(r.name.lower() in ["админ", "модер", "состав", "admin", "mod", "support"] for r in interaction.user.roles)
        if not (is_admin or has_role):
            await interaction.response.send_message("❌ Закрыть может только Админ/Модер!", ephemeral=True)
            return
        await interaction.response.send_message("🔒 Закрывается через 5 сек...")
        await asyncio.sleep(5)
        await interaction.channel.delete()

class TicketSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Пожаловаться на пользователя", emoji="👤"),
            discord.SelectOption(label="Пожаловаться на состав", emoji="👮"),
            discord.SelectOption(label="Подать заявку на должность", emoji="📝"),
            discord.SelectOption(label="Другое...", emoji="❓"),
        ]
        super().__init__(placeholder="Выберите тему", min_values=1, max_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites, category=interaction.channel.category if interaction.channel.category else None)
        embed = discord.Embed(title=f"🎫 Тикет: {self.values[0]}", description=f"{interaction.user.mention} Опиши проблему! Тема: {self.values[0]}", color=0x2B2D31)
        await channel.send(embed=embed, view=CloseTicketView())
        await interaction.response.send_message(f"✅ Тикет: {channel.mention}", ephemeral=True)

class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.event
async def on_ready():
    print(f"Бот онлайн {bot.user}")

@bot.command(name="поддержка")
async def support(ctx):
    if ctx.channel.name.lower()!= "поддержка":
        await ctx.send("❌ Только в #поддержка!", delete_after=5)
        return
    embed = discord.Embed(title="🔥 Обратиться в поддержку", description="Выберите тему тикета в меню и заполните форму. Постарайтесь предоставить как можно больше информации в своем запросе.", color=0x2B2D31)
    await ctx.send(embed=embed, view=TicketView())

bot.run(TOKEN)
