from os import name
import discord
from discord.activity import Spotify
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import datetime
from discord import Spotify
import requests
import random

warning_color = 0xff0400


class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name="ban", description="This command is used to ban user.")
    async def slash_ban(self, ctx: SlashContext, member: discord.Member, *, reason=None):
        if ctx.guild.me.top_role.position < member.top_role.position or member == ctx.guild.owner:
            await ctx.send("I can't ban Owner/Modeartors/Staff.")
            return
        # with open("./json/config.json", "r") as json_file:
        #     config = json.load(json_file)
        # try:
        #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
        #                           ]["Configuration"]["Logchannel"]
        #     log_channel = self.client.get_channel(id=logchanel_id)
        # except KeyError:
        #     log_channel = ctx.channel
        if reason is None:
            reason = "No reason provided"
        await member.send(f"You got banned from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
        await member.ban(reason=reason)
        ban_embed = discord.Embed(title="Member banned", colour=warning_color)
        ban_embed.add_field(nmae="Member ID : ||{member.id}||")
        ban_embed.add_field(name="User", value=member.name)
        ban_embed.add_field(
            name="Banned by", value=ctx.author.name, inllne=True)
        ban_embed.add_field(name="Reason", value=reason, inllne=True)
        ban_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=ban_embed)

    @cog_ext.cog_slash(name="kick", description="This command is used to kick someone from the server.")
    async def slash_kick(self, ctx: SlashContext, member: discord.Member, *, reason=None):
        if ctx.guild.me.top_role.position < member.top_role.position or member == ctx.guild.owner:
            await ctx.send("I can't ban Owner/Modeartors/Staff.")
            return
        # with open("./json/config.json", "r") as json_file:
        #     config = json.load(json_file)
        # try:
        #     logchanel_id = config[("Guild_ID_" + str(ctx.guild.id))
        #                           ]["Configuration"]["Logchannel"]
        #     log_channel = self.client.get_channel(id=logchanel_id)
        # except KeyError:
        #     log_channel = ctx.channel
        if reason is None:
            reason = "No reason provided"
        await member.send(f"You got Kicked from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
        await member.kick(reason=reason)
        kick_embed = discord.Embed(
            title="Member Kicked!", colour=warning_color)
        kick_embed.add_field(name="Member ID ", value=member.id, inline=False)
        kick_embed.add_field(name="User", value=member.name, inline=False)
        kick_embed.add_field(
            name="Kicked by", value=ctx.author.name, inline=True)
        kick_embed.add_field(name="Reason", value=reason, inline=True)
        kick_embed.set_thumbnail(url=member.avatar_url)
        kick_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=kick_embed)

    @cog_ext.cog_slash(name="Spotify", description="")
    async def spotify(ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
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

    @cog_ext.cog_slash(name="joke", description="Sends joke")
    async def joke(ctx):
        req = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = req.json()
        embed = discord.Embed(
            title="{}".format(joke['setup']),
            description="{}".format(joke['punchline']),
            color=0xFF5733)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="insult", description="")
    async def insult(ctx, user: discord.Member = None):
        if user is None:
            await ctx.send("No u cant insult yourself,Tag someone")
        else:
            req = requests.get(
                "https://evilinsult.com/generate_insult.php?lang=en&type=json")
            insult = req.json()
            embed = discord.Embed(title="{}".format(user.display_name),
                                  description="{}".format(insult['insult']),
                                  color=0xFF5733)
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="createavatar", description="Creates avatar from random characters")
    async def createavatar(ctx, a=None):
        if a is None:
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

    # to send avatar of the user

    @cog_ext.cog_slash(name="avatar", description="sends user avatar")
    async def av(ctx, user: discord.User = None):
        if isinstance(user, commands.UserNotFound):
            await ctx.send("Hmm 🤔, I had a hard time finding the user, you sure that user exits❓ it got a bit chilly right now 👻")

        else:
            await ctx.send("Hmm somethings wrong, plz inform the developers")

        emb = discord.Embed(title="Avatar")

        if user is None:
            emb.set_image(url=ctx.author.avatar_url)

        else:
            emb.set_image(url=user.avatar_url)

        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(Slash(client))
    print(" <Slash commands loaded>")
