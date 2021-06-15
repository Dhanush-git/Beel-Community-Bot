import discord
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
            await ctx.send("I can't ban Owner/Moderators/Staff.")
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
        await member.send(
            f"You got banned from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
        await member.ban(reason=reason)
        ban_embed = discord.Embed(title="Member banned", colour=warning_color)
        ban_embed.add_field(name="Member ID", value=member.id, inline=False)
        ban_embed.add_field(name="User", value=member.name, inline=False)
        ban_embed.add_field(
            name="Banned by", value=ctx.author.name, inline=False)
        ban_embed.add_field(name="Reason", value=reason, inline=False)
        ban_embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=ban_embed)

    @cog_ext.cog_slash(name="kick", description="This command is used to kick someone from the server.")
    async def slash_kick(self, ctx: SlashContext, member: discord.Member, *, reason=None):
        if ctx.guild.me.top_role.position < member.top_role.position or member == ctx.guild.owner:
            await ctx.send("I can't ban Owner/Moderators/Staff.")
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
        await member.send(
            f"You got Kicked from server **{ctx.guild.name}** by **{ctx.author.name}** for reason: `{reason}`")
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

    @cog_ext.cog_slash(name="unlock channel")
    async def slash_lock(self, ctx: SlashContext, role: discord.Role):
        await ctx.channel.set_permissions(role, send_messages=False, read_messages=True)
        await ctx.send("Channel locked.", delete_after=10)

    @cog_ext.cog_slash(name="lock channel", description="Locks channel for a role.")
    async def slash_unlock(self, ctx: SlashContext, role: discord.Role):
        await ctx.channel.set_permissions(role, send_messages=True, read_messages=True)
        await ctx.send("Channel unlocked.", delete_after=10)

    @cog_ext.cog_slash(name='clear', description='clears messages in any channel.')
    async def slash_clear(self, ctx: SlashContext, amount1: int = 10):
        channel = ctx.message.channel
        if 0 < amount1 <= 100:
            await channel.purge(limit=amount1)

        else:
            await ctx.send("Limit provided is not in range.")

    @cog_ext.cog_slash(name='clearuser', description="Clear messages of particular user in a channel")
    async def slash_purgeuser(self, ctx: SlashContext, user: discord.Member = None, num_messages: int = None):
        if num_messages is None:
            num_messages = 100
        user = user or ctx.author
        channel = ctx.message.channel
        if ctx.guild.me.top_role < user.top_role or ctx.message.author.top_role < user.top_role:
            return await ctx.send("Sorry!, I can't clear messages of Owner/staff/moderators.")

        def check(msg):
            return msg.author.id == user.id

        await ctx.message.delete()
        await channel.purge(limit=num_messages, check=check, before=None)

    @cog_ext.cog_slash(name="Spotify")
    async def slash_spotify(self, ctx: SlashContext, user: discord.Member = None):
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
    async def slash_joke(self, ctx: SlashContext):
        req = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = req.json()
        embed = discord.Embed(
            title="{}".format(joke['setup']),
            description="{}".format(joke['punchline']),
            color=0xFF5733)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="createavatar", description="Creates avatar from random characters")
    async def slash_createavatar(self, ctx: SlashContext, a=None):
        if a is None:
            await ctx.send("please enter a random text to generate your avatar")
        else:
            req = requests.get(
                f'https://robohash.org/{a}.png?set=set{random.randint(1, 3)}')
            img = req.url
            embed = discord.Embed(title="your avatar",
                                  description=f"Here is your random avatar generated by your text {a}",
                                  color=0xFF5733)
            embed.set_image(url=img)
            embed.set_footer(text="created by https://robohash.org/")
            await ctx.send(embed=embed)

    # to send avatar of the user

    @cog_ext.cog_slash(name="avatar", description="sends user avatar")
    async def slash_av(self, ctx: SlashContext, user: discord.User = None):
        if isinstance(user, commands.UserNotFound):
            await ctx.send(
                "Hmm 🤔, I had a hard time finding the user, you sure that user exits❓ it got a bit chilly right now 👻")
            return

        emb = discord.Embed(title="Avatar")

        if user is None:
            emb.set_image(url=ctx.author.avatar_url)

        else:
            emb.set_image(url=user.avatar_url)

        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @commands.Cog.listener()
    async def on_ready(self):
        print(" <Slash commands loaded>")


def setup(client):
    client.add_cog(Slash(client))
