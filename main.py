import discord
from discord.ext import commands
from decouple import config
import random


TOKEN = config("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(name="roll")
async def roll(ctx, *, args: str):
    try:
        n, x = map(int, args.split("d"))
    except ValueError:
        await ctx.send("Comando inválido.")
        return
    results = [random.randint(1, x) for _ in range(n)]
    await ctx.send(f"`{sum(results)}` -> ({', '.join(str(x) for x in results)})")


bot.run(TOKEN)
