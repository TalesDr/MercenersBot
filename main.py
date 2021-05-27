from datetime import datetime
import time
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import numpy as np

#variables globales

load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, description="Bot des MERCENERS", help_command=None)
guild = bot.get_guild(813039372680691722)

@bot.command()
async def commande(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour=discord.Colour.orange()
    )
    embed.set_author(name='Liste des commandes')
    embed.add_field(name="!purge", value="Renvoi un CSV avec les ID des membres inactifs", inline=False)
    embed.add_field(name="!list-id", value="Renvoi un CSV avec les ID des membres", inline=True)
    embed.add_field(name="!membres", value="Affiche le nombre de membres sur le serveur", inline=False)

    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    caca = "caca"
    choco = "chocolatine"
#commandes funs
    if message.content.lower() == "ping":
        await message.channel.send("pong")
    if choco in message.content.lower():
        await message.channel.send(f'{message.author.display_name} vous avez une amende d\'un crédit pour infraction au code de moralité du langage.')
    if caca in message.content.lower():
        await message.channel.send("💩")

#enregistre dans un fichier la liste des message avec date et id membre
    with open("files/stats.csv", "a") as f:
        now = datetime.now()
        f.write(f"{int(time.time())}, {message.author.id}\n")
        await bot.process_commands(message)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Destiny 2"))
    print('We have logged in as {0.user}'.format(bot))

#renvoie la listes des membres du serveur
@bot.command()
async def list_id(ctx):
    guild = bot.get_guild(813039372680691722)
    with open("files/member.csv", "w") as f:
        for member in guild.members:
                f.write(f"{member.id},\n")
    await ctx.send("Voici la liste")
    await ctx.send(file=discord.File('files/member.csv'))

#verifie que celui qui parle n'est pas le bot
    if ctx.author == bot.user:
        return

#renvoie nombres de membres
@bot.command()
async def membres(ctx):
    guild = bot.get_guild(813039372680691722)
    await ctx.send(f'Nombres de membres : {guild.member_count}')

#fonction pour calculer les id uniques
def unique(list1):
    x = np.array(list1)
    #print(np.unique(x))
    result = np.unique(x)
    return result

#fonction pour afficher les membres inactifs depuis 30 jours
@bot.command()
async def purge(ctx):
    #hour = int(time.time()) - 3600
    #day = int(time.time()) - 86400
    month = int(time.time()) - 2629743
    membres = [] #id des membres totaux
    id_messages = []#id des membres dont les messages date de moins de 30 jours
    guild = bot.get_guild(813039372680691722)
    with open("files/member.csv", "w") as f:
        for member in guild.members:
            f.write(f"{member.id},\n")
    with open("files/member.csv", 'r') as g:
        for line in g:
            membres.append(line[0:18])
    with open("files/stats.csv", "r") as f:
        for row in f:
            date = row[0:10]
            if int(date) > month:
                id_membre = [row[12:30]]
                id_messages.extend(id_membre)
    id_unique = unique(id_messages)
    s1 = set(id_unique)
    s2 = set(membres)
    s3 = s1.symmetric_difference(s2)
    with open('files/inactifs.csv', 'w') as h:
        for row in s3:
            h.write(f'{row}\n')
    await ctx.send(f'ACTIFS : {len(s1)}')
    await ctx.send(f'INACTIFS : {len(s3)}')
    await ctx.send(file=discord.File('files/inactifs.csv'))


bot.run(os.getenv("TOKEN"))