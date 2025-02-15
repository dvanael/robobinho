import discord
import random
import requests
from discord.ext import commands
from decouple import config


TOKEN = config("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


# @bot.event
# async def on_message(message):
#     print(f"Message from {message.author}: {message.content}")


@bot.command(name="hello")
async def hello(ctx):
    await ctx.send(f"Olá, {ctx.author.mention}!")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(name="love")
async def mark(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} ama {member.mention}! <3")


@bot.command(name="pkmn")
async def pkmn(ctx, *, args: str):
    print("Starting PokeAPI request...")
    poke_api_url = f"https://pokeapi.co/api/v2/pokemon/{args}"
    response = requests.get(poke_api_url)
    print(f"PokeAPI {response.status_code}")

    if response.status_code != 200:
        await ctx.send("PokeAPI retornou um erro.")
        return

    elif response.status_code == 200:
        data = response.json()
        embed = discord.Embed(
            title=data["name"], description=f"Pokémon N° {data['id']}", color=0xF24153
        )

        sprite = data["sprites"]["versions"]["generation-v"]["black-white"]["animated"][
            "front_default"
        ]
        embed.set_image(url=sprite)

    await ctx.send(embed=embed)


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
