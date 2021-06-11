from logging import error
import os
import discord
from discord.ext import commands


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

@client.event
async def on_command_error(ctx, error):
    raise error


extensions = ["cogs.automod"]
for e in extensions:
    client.load_extension(e)

    
client.run(os.getenv('TOKEN'))
