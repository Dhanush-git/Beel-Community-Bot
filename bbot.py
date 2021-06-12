import os
import discord
import requests
import random
import discord.ext
from discord.ext import commands
from discord import Spotify

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


client = commands.Bot(command_prefix="bb", intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.event
async def on_message(msg):

    if client.user.mentioned_in(msg):

        # Bot responds with the current prefix when mentioned in the message
        # "#009aff" or 0x009aff if the color used for Beel
        emb = discord.Embed(
            description=f"Hi, I currently respond to\n```Prefix: bb```", color=0x009aff)
        await msg.channel.send(embed=emb)

    await client.process_commands(msg)


@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")


@client.command()
async def ping(ctx):

    await ctx.channel.send(f"Pong {round(client.latency*1000)} ms")


@client.command()
async def spotify(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
        pass
    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                embed = discord.Embed(
                    title=f"{user.name}'s Spotify",
                    description="Listening to {}".format(activity.title),
                    color=activity.colour)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                embed.set_footer(text="Song started at {}".format(
                    activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=embed)
    else:
        await ctx.send("user is not listening to any song ")


@client.command()
async def joke(ctx):
    req = requests.get("https://official-joke-api.appspot.com/random_joke")
    joke = req.json()
    embed = discord.Embed(
        title="{}".format(joke['setup']),
        description="{}".format(joke['punchline']),
        color=0xFF5733)
    await ctx.send(embed=embed)


@client.command()
async def insult(ctx, user: discord.Member = None):
    if user == None:
        await ctx.send("No u cant insult yourself,Tag someone")
    else:
        req = requests.get(
            "https://evilinsult.com/generate_insult.php?lang=en&type=json")
        insult = req.json()
        embed = discord.Embed(title="{}".format(user.display_name),
                              description="{}".format(insult['insult']),
                              color=0xFF5733)
        await ctx.send(embed=embed)


@client.command()
async def createavatar(ctx, a=None):
    if a == None:
        await ctx.send("please enter a random text to generate your avatar")
    else:
        req = requests.get(
            f'https://robohash.org/{a}.png?set=set{random.randint(1,3)}')
        img = req.url
        embed = discord.Embed(title="your avatar",
                              description=f"Here is your random avatar genrated by your text {a}",
                              color=0xFF5733)
        embed.set_image(url=img)
        embed.set_footer(text="created by https://robohash.org/")
        await ctx.send(embed=embed)



#to send avatar of the user
@client.command()
async def av(ctx, user: discord.User = None):

    emb = discord.Embed(title="Avatar")

    if user == None:
        emb.set_image(url=ctx.author.avatar_url)

    else:
        emb.set_image(url=user.avatar_url)

    emb.set_author(name=ctx.author , icon_url=ctx.author.avatar_url)
    await ctx.send(embed=emb)

@av.error
async def av_error(ctx, error):
    if isinstance(error , commands.UserNotFound):
        await ctx.send("Hmm 🤔, I had a hard time finding the user, you sure that user exits❓ it got a bit chilly right now 👻")

    else:
        await ctx.send("Hmm somethings wrong, plz inform the developers")




client.run(os.getenv('TOKEN'))
