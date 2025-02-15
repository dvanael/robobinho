import discord
import requests
from discord.ext import commands
from decouple import config
from utils.roll import roll_dice

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
    results = roll_dice(n, x)
    await ctx.send(f"`{sum(results)}` -> ({', '.join(str(x) for x in results)})")


@bot.command(name="spell")
async def spell(ctx, *, args: str):
    print("Starting DnD API request...")
    dnd_api_url = f"http://localhost:8000/api/spells/{args}"
    response = requests.get(dnd_api_url)
    print(f"DnD API {response.status_code}")

    if response.status_code != 200:
        await ctx.send("DnD API retornou um erro.")
        return

    elif response.status_code == 200:
        spell = response.json()

        nome_magia = spell["name"]
        descricao_magia = spell["desc"][0]

        embed = discord.Embed(
            title=f"✨ {nome_magia.capitalize()}",
            description=descricao_magia,
        )
        embed.add_field(name="🔹 Nível", value=f"{spell["level"]}° nível", inline=True)
        embed.add_field(name="🔹 Escola", value=spell["school"]["name"], inline=True)
        embed.add_field(
            name="🔹 Tempo de Conjuração",
            value=spell["casting_time"],
            inline=False,
        )
        embed.add_field(name="🔹 Alcance", value=spell["range"], inline=True)
        embed.add_field(
            name="🔹 Componentes",
            value=f"{', '.join(str(x) for x in spell["components"])}",
            inline=True,
        )
        embed.add_field(name="🔹 Duração", value=spell["duration"], inline=True)

        if "damage" in spell:
            spell_damage_dice = spell["damage"]["damage_at_slot_level"][
                f"{spell['level']}"
            ]
            n, x = spell_damage_dice.split("d")
            total_damage = roll_dice(int(n), int(x))
            embed.add_field(
                name="🔥 Dano Causado",
                value=f" `{sum(total_damage)} de dano de {spell['damage']['type']['name']}` ({', '.join(str(x) for x in total_damage)})",
                inline=False,
            )

        if "heal_at_slot_level" in spell:
            spell_heal_dice = spell["heal_at_slot_level"][f"{spell['level']}"]
            if "d" in spell_heal_dice:
                n, x = spell_heal_dice.split("d")
                total_heal = roll_dice(int(n), int(x))
                embed.add_field(
                    name="❤️ Cura",
                    value=f" `{sum(total_heal)} de cura` ({', '.join(str(x) for x in total_heal)})",
                    inline=False,
                )
            else:
                total_heal = [int(spell_heal_dice)]
                embed.add_field(
                    name="❤️ Cura",
                    value=f" `{sum(total_heal)} de cura`",
                    inline=False,
                )

    await ctx.send(embed=embed)


bot.run(TOKEN)
