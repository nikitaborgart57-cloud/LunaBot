import discord, os
from discord import ui
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

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
        channel = await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
        embed = discord.Embed(title=f"🎫 {self.values[0]}", description=f"{interaction.user.mention} Тикет создан!\n**Тема:** {self.values[0]}\nОпиши подробно свою ситуацию.", color=0x2B2D31)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Твой тикет: {channel.mention}", ephemeral=True)

class TicketView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())

@bot.event
async def on_ready():
    print(f"LunaBot 24/7 онлайн как {bot.user}")

@bot.command()
async def поддержка(ctx):
    embed = discord.Embed(title="Обратиться в поддержку", description="Выберите тему тикета в меню и заполните форму. Постарайтесь предоставить как можно больше информации в своем запросе.", color=0x2B2D31)
    await ctx.send(embed=embed, view=TicketView())

bot.run(TOKEN)
