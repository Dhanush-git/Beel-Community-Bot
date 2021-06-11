import os
import discord
from discord.ext import commands
from discord import Spotify

from dotenv import load_dotenv , find_dotenv

load_dotenv(find_dotenv())



client = commands.Bot(command_prefix="bb",intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")

@client.event
async def on_message(msg):

    if client.user.mentioned_in(msg):

        #Bot responds with the current prefix when mentioned in the message
        # "#009aff" or 0x009aff if the color used for Beel
        emb = discord.Embed(description=f"Hi, I currently respond to\n```Prefix: bb```",color=0x009aff)
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
                    title = f"{user.name}'s Spotify",
                    description = "Listening to {}".format(activity.title),
                    color = activity.colour)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="Artist", value=activity.artist)
                embed.add_field(name="Album", value=activity.album)
                embed.set_footer(text="Song started at {}".format(activity.created_at.strftime("%H:%M")))
                await ctx.send(embed=embed)
    else:
        await ctx.send("user is not listening to any song ")


client.run(os.getenv('TOKEN'))
